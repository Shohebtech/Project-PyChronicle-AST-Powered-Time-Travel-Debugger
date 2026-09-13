from storage.sqlite_storage import SQLiteStorage


storage = SQLiteStorage()

storage.create_tables()

storage.insert_state(
    1.0,
    10,
    "x",
    "100"
)

print("Execution state inserted successfully.")

storage.close()