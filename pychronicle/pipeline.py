import os
import sys
import time

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tracer import tracer as tracer_module
from storage.sqlite_storage import SQLiteStorage


EMPTY_STATE_VARIABLE = "__pychronicle_empty_state__"


def run_pipeline(filepath, db_path="pychronicle.db"):
    storage = SQLiteStorage(db_path)
    storage.create_tables()
    storage.clear_history()

    try:
        tracer_module.run_tracer(filepath)
        history = tracer_module.execution_history

        position = 0
        for record in history:
            if record["event"] != "LINE":
                continue

            line_number = record["line"]
            variables = record["variables"]

            states = (
                variables.items()
                if variables
                else ((EMPTY_STATE_VARIABLE, {}),)
            )
            for variable_name, value in states:
                serialized_value = storage.serialize_value(value)
                storage.insert_state(
                    position,
                    time.time(),
                    line_number,
                    variable_name,
                    serialized_value
                )

            position += 1
    finally:
        storage.close()

    print(f"Pipeline complete: {position} execution point(s) written to {db_path}")

    return position


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <script.py>")
        sys.exit(1)

    run_pipeline(sys.argv[1])