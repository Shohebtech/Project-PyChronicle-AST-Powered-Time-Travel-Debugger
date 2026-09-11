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

    def close(self):
        # Close the database connection
        self.connection.close()