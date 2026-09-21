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


print("\nTesting delta storage:")

print(storage.insert_delta_state(3.0, 20, "x", "100"))
print(storage.insert_delta_state(4.0, 21, "x", "100"))
print(storage.insert_delta_state(5.0, 22, "x", "200"))


storage.close()

print("Storage test completed successfully.")