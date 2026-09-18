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

        # Save the table creation
        self.connection.commit()

    def insert_state(
        self,
        timestamp,
        line_number,
        variable_name,
        serialized_value
    ):
        # Create a cursor to execute SQL commands
        cursor = self.connection.cursor()

        # Insert one execution state into the database
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

        # Save the inserted data
        self.connection.commit()

    def get_all_states(self):
        # Create a cursor to execute SQL commands
        cursor = self.connection.cursor()

        # Retrieve all stored execution states
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

        # Return all execution states
        return cursor.fetchall()

    def get_states_until(self, execution_id):
        # Create a cursor to execute SQL commands
        cursor = self.connection.cursor()

        # Retrieve execution states up to the selected execution ID
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

        # Return historical execution states
        return cursor.fetchall()

    def serialize_value(self, value):
        # Convert Python value into a storable format
        return str(value)

    def deserialize_value(self, value):
        # Convert stored value back into a Python value
        return value

    def close(self):
        # Close the database connection
        self.connection.close()