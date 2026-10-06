import time

from storage.sqlite_storage import SQLiteStorage


# Create storage
storage = SQLiteStorage("test_pychronicle.db")

# Create database tables
storage.create_tables()


# --------------------------------------------------
# 1. Test normal state insertion
# --------------------------------------------------

print("\nTesting state insertion:")

storage.insert_state(
    1,
    1.0,
    10,
    "x",
    "100"
)

storage.insert_state(
    2,
    2.0,
    15,
    "y",
    "200"
)

print("States inserted successfully.")


# --------------------------------------------------
# 2. Test retrieving all states
# --------------------------------------------------

print("\nTesting get_all_states:")

states = storage.get_all_states()

print("Number of stored states:", len(states))

for state in states:
    print(state)


# --------------------------------------------------
# 3. Test historical state retrieval
# --------------------------------------------------

print("\nTesting get_states_until:")

historical_states = storage.get_states_until(1)

print("States until position 1:")

for state in historical_states:
    print(state)


# --------------------------------------------------
# 4. Test delta-based storage
# --------------------------------------------------

print("\nTesting delta storage:")

result1 = storage.insert_delta_state(
    3,
    3.0,
    20,
    "x",
    "100"
)

print("First x insertion:", result1)

result2 = storage.insert_delta_state(
    4,
    4.0,
    21,
    "x",
    "100"
)

print("Same x value:", result2)

result3 = storage.insert_delta_state(
    5,
    5.0,
    22,
    "x",
    "200"
)

print("Changed x value:", result3)


# --------------------------------------------------
# 5. Test batch insertion
# --------------------------------------------------

print("\nTesting batch insertion:")

batch_states = [
    (6, 6.0, 30, "a", "10"),
    (7, 7.0, 35, "b", "20"),
    (8, 8.0, 40, "c", "30")
]

result = storage.insert_many_states(batch_states)

print("Number of batch states inserted:", result)


# --------------------------------------------------
# 6. Test performance
# --------------------------------------------------

print("\nTesting storage performance:")

performance_states = []

for i in range(1000):
    performance_states.append(
        (
            i + 9,
            float(i + 9),
            i,
            f"variable_{i % 10}",
            str(i)
        )
    )

start_time = time.time()

storage.insert_many_states(performance_states)

end_time = time.time()

elapsed_time = end_time - start_time

print("Inserted 1000 states successfully.")
print("Insertion time:", round(elapsed_time, 4), "seconds")


# --------------------------------------------------
# 7. Test empty batch
# --------------------------------------------------

print("\nTesting empty batch:")

empty_result = storage.insert_many_states([])

print("Empty batch result:", empty_result)


# --------------------------------------------------
# 8. Test variable history
# --------------------------------------------------

print("\nTesting variable history:")

x_history = storage.get_variable_history("x")

print("History of variable x:")

for state in x_history:
    print(state)


# --------------------------------------------------
# 9. Test serialization
# --------------------------------------------------

print("\nTesting serialization:")

original_value = {
    "name": "Harini",
    "marks": [80, 90, 95]
}

serialized_value = storage.serialize_value(original_value)

print("Serialized value:", serialized_value)

deserialized_value = storage.deserialize_value(serialized_value)

print("Deserialized value:", deserialized_value)


# --------------------------------------------------
# 10. Close database
# --------------------------------------------------

storage.close()

print("\nStorage test completed successfully.")