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

states = storage.get_all_states()

print("\nStored execution states:")

for state in states:
    print(state)

storage.close()