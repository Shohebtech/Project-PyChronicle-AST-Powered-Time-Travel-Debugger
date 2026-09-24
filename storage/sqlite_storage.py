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
                timestamp REAL NOT NULL,
                line_number INTEGER NOT NULL,
                variable_name TEXT NOT NULL,
                serialized_value TEXT
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_execution_states_variable
            ON execution_states(variable_name)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_execution_states_line
            ON execution_states(line_number)
        """)

        # Save the table creation
        self.connection.commit()

    def insert_state(
        self,
        timestamp,
        line_number,
        variable_name,
        serialized_value
    ):
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                INSERT INTO execution_states
                (timestamp, line_number, variable_name, serialized_value)
                VALUES (?, ?, ?, ?)
            """, (
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
        try:
            cursor = self.connection.cursor()

            cursor.executemany("""
                INSERT INTO execution_states
                (timestamp, line_number, variable_name, serialized_value)
                VALUES (?, ?, ?, ?)
            """, states)

            self.connection.commit()

        except sqlite3.Error as error:
            self.connection.rollback()
            print("Error inserting multiple states:", error)

    def insert_delta_state(
        self,
        timestamp,
        line_number,
        variable_name,
        serialized_value
    ):
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
                    (timestamp, line_number, variable_name, serialized_value)
                    VALUES (?, ?, ?, ?)
                """, (
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

    def get_all_states(self):
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    timestamp,
                    line_number,
                    variable_name,
                    serialized_value
                FROM execution_states
                ORDER BY id
            """)

            return cursor.fetchall()

        except sqlite3.Error as error:
            print("Error retrieving execution states:", error)
            return []

    def get_states_until(self, execution_id):
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    timestamp,
                    line_number,
                    variable_name,
                    serialized_value
                FROM execution_states
                WHERE id <= ?
                ORDER BY id
            """, (execution_id,))

            return cursor.fetchall()

        except sqlite3.Error as error:
            print("Error retrieving historical states:", error)
            return []

    def serialize_value(self, value):
        # Convert Python value into a storable format
        return str(value)

    def deserialize_value(self, value):
        # Convert stored value back into a Python value
        return value

    def close(self):
        try:
            self.connection.close()
        except sqlite3.Error as error:
            print("Error closing database connection:", error)