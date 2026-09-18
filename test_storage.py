from storage.sqlite_storage import SQLiteStorage


storage = SQLiteStorage("test_pychronicle.db")

storage.create_tables()

storage.insert_state(
    1.0,
    10,
    "x",
    "100"
)

storage.insert_state(
    2.0,
    15,
    "y",
    "200"
)

states = storage.get_all_states()

print("Number of stored states:", len(states))

for state in states:
    print(state)

storage.close()

print("Storage test completed successfully.")