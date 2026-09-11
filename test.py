from storage.sqlite_storage import SQLiteStorage


storage = SQLiteStorage()

storage.create_tables()

print("SQLite database and table created successfully.")

storage.close()