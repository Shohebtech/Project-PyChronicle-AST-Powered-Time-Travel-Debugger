import time

from tracer import tracer as tracer_module
from storage.sqlite_storage import SQLiteStorage


def run_pipeline(filepath, db_path="pychronicle.db"):
    
    tracer_module.run_tracer(filepath)

    history = tracer_module.execution_history

    storage = SQLiteStorage(db_path)
    storage.create_tables()

    position = 0
    for record in history:
        if record["event"] != "LINE":
            continue

        line_number = record["line"]
        variables = record["variables"]

        for variable_name, value in variables.items():
            serialized_value = storage.serialize_value(value)
            storage.insert_state(
                position,
                time.time(),
                line_number,
                variable_name,
                serialized_value
            )

        position += 1

    storage.close()
    print(f"Pipeline complete: {position} execution point(s) written to {db_path}")

    return position


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <script.py>")
        sys.exit(1)

    run_pipeline(sys.argv[1])