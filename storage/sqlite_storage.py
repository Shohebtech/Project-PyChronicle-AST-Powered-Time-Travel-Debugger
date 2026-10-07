import json
import sqlite3


class SQLiteStorage:

    def __init__(self, db_path="pychronicle.db"):
        # Store the database file path
        self.db_path = db_path

        # Create a connection to the SQLite database
        self.connection = sqlite3.connect(self.db_path)

    def create_tables(self):
        # Create a cursor to execute SQL commands
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS execution_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                position INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                line_number INTEGER NOT NULL,
                variable_name TEXT NOT NULL,
                serialized_value TEXT
            )
        """)
        # NOTE: added "position INTEGER NOT NULL" above - the TUI (Member 4)
        # needs this to navigate execution history as an ordered sequence
        # (0, 1, 2, 3...), separate from "timestamp" which records the
        # real-world time a change happened. Both are useful, so this keeps
        # timestamp and adds position alongside it, rather than replacing it.

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_execution_states_variable
            ON execution_states(variable_name)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_execution_states_line
            ON execution_states(line_number)
        """)

        # NEW: an index on position, since the TUI will query/order by it
        # constantly (next/previous navigation, jumping to a specific point).
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_execution_states_position
            ON execution_states(position)
        """)

        # Save the table creation
        self.connection.commit()

    def clear_history(self):
        try:
            self.connection.execute("DELETE FROM execution_states")
            self.connection.commit()
        except sqlite3.Error as error:
            self.connection.rollback()
            print("Error clearing execution history:", error)

    def insert_state(
        self,
        position,
        timestamp,
        line_number,
        variable_name,
        serialized_value
    ):
        # NOTE: added "position" as the first parameter.
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                INSERT INTO execution_states
                (position, timestamp, line_number, variable_name, serialized_value)
                VALUES (?, ?, ?, ?, ?)
            """, (
                position,
                timestamp,
                line_number,
                variable_name,
                serialized_value
            ))

            self.connection.commit()

        except sqlite3.Error as error:
            self.connection.rollback()
            print("Error inserting execution state:", error)

    def insert_many_states(self, states):
        # NOTE: each tuple in "states" must now be
        # (position, timestamp, line_number, variable_name, serialized_value)
        # instead of the previous 4-value shape.
        if not states:
            return 0

        try:
            cursor = self.connection.cursor()

            cursor.executemany("""
                INSERT INTO execution_states
                (position, timestamp, line_number, variable_name, serialized_value)
                VALUES (?, ?, ?, ?, ?)
            """, states)

            self.connection.commit()

            return cursor.rowcount

        except sqlite3.Error as error:
            self.connection.rollback()
            print("Error inserting multiple states:", error)
            return 0

    def insert_delta_state(
        self,
        position,
        timestamp,
        line_number,
        variable_name,
        serialized_value
    ):
        # NOTE: added "position" as the first parameter.
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                SELECT serialized_value
                FROM execution_states
                WHERE variable_name = ?
                ORDER BY id DESC
                LIMIT 1
            """, (variable_name,))

            previous_state = cursor.fetchone()

            if previous_state is None or previous_state[0] != serialized_value:
                cursor.execute("""
                    INSERT INTO execution_states
                    (position, timestamp, line_number, variable_name, serialized_value)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    position,
                    timestamp,
                    line_number,
                    variable_name,
                    serialized_value
                ))

                self.connection.commit()
                return True

            return False

        except sqlite3.Error as error:
            self.connection.rollback()
            print("Error inserting delta state:", error)
            return False

    def get_variable_history(self, variable_name):
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    position,
                    timestamp,
                    line_number,
                    variable_name,
                    serialized_value
                FROM execution_states
                WHERE variable_name = ?
                ORDER BY position
            """, (variable_name,))
            # NOTE: now selects + orders by "position" too, since that's
            # the meaningful execution order the TUI will want, rather
            # than relying on "id" (which happens to match today, but
            # isn't guaranteed to mean the same thing).

            return cursor.fetchall()

        except sqlite3.Error as error:
            print("Error retrieving variable history:", error)
            return []

    def get_all_states(self):
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    position,
                    timestamp,
                    line_number,
                    variable_name,
                    serialized_value
                FROM execution_states
                ORDER BY position
            """)

            return cursor.fetchall()

        except sqlite3.Error as error:
            print("Error retrieving execution states:", error)
            return []

    def get_states_until(self, position):
        # NOTE: renamed parameter from "execution_id" to "position" and the
        # query now filters/orders by position instead of id, so "give me
        # everything up to this point" means execution order, matching how
        # the TUI actually thinks about history (position-based, not
        # database-row-based).
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    position,
                    timestamp,
                    line_number,
                    variable_name,
                    serialized_value
                FROM execution_states
                WHERE position <= ?
                ORDER BY position
            """, (position,))

            return cursor.fetchall()

        except sqlite3.Error as error:
            print("Error retrieving historical states:", error)
            return []

    def serialize_value(self, value):
        # Convert Python value into a storable format.
        # Uses JSON (not plain str()) because Member 4's TUI adapter
        # (storage_adapter.py) reads stored values back with json.loads().
        # json.dumps() ensures numbers, strings, booleans, lists, and
        # dicts all round-trip correctly - e.g. str("hello") would store
        # as hello (no quotes), which json.loads() can't parse back into
        # a string; json.dumps("hello") correctly stores "hello".
        try:
            return json.dumps(value)
        except TypeError:
            # Fallback for values json can't serialize directly
            # (e.g. custom objects) - stored as plain text instead.
            return json.dumps(str(value))

    def deserialize_value(self, value):
        # Convert stored value back into a Python value.
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    def close(self):
        try:
            self.connection.close()
        except sqlite3.Error as error:
            print("Error closing database connection:", error)
