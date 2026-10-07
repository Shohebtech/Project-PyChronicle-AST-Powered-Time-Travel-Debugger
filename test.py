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

historical_states = storage.get_states_until(2)

print("\nHistorical states up to execution ID 2:")

for state in historical_states:
    print(state)
value = [10, 20, 30]

serialized = storage.serialize_value(value)
print("Serialized value:", serialized)

deserialized = storage.deserialize_value(serialized)
print("Deserialized value:", deserialized)

storage.close()