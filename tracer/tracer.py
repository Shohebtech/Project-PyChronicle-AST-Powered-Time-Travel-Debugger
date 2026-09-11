import sys
import os

previous_variables = {}

step = 0
TARGET_FILE = None
execution_history = []


def tracer(frame, event, arg):
    global step
    global previous_variables

    # Trace only target Python file
    if frame.f_code.co_filename != TARGET_FILE:
        return tracer

    if event == "line":

        step += 1

        current_variables = {
            key: value
            for key, value in frame.f_locals.items()
            if key != "__builtins__"
        }

        changes = {}

        #these will remove the unecessary built-in variales
        variables = {
            key: value
            for key, value in frame.f_locals.items()
            if key != "__builtins__"
        }

         # Check new and modified variables
        for key, value in current_variables.items():

            if key not in previous_variables:
                changes[key] = {
                    "type": "NEW",
                    "value": value
                }

            elif previous_variables[key] != value:
                changes[key] = {
                    "type": "MODIFIED",
                    "old": previous_variables[key],
                    "new": value
                }

         # Check removed variables
        for key in previous_variables:

            if key not in current_variables:
                changes[key] = {
                    "type": "REMOVED",
                    "old": previous_variables[key]
                }


        record = {
            "step": step,
            "event": event,
            "line": frame.f_lineno,
            "function": frame.f_code.co_name,
            "variables": variables
        }

        # print(
        #     "LINE:",
        #     frame.f_lineno,
        #     "FUNCTION:",
        #     frame.f_code.co_name,
        #     # "VARS:",
        #     # frame.f_locals
        #     "VARS:",
        #     variables
        # )

        print(
            "LINE:",
            frame.f_lineno,
            "FUNCTION:",
            frame.f_code.co_name,
            "VARS:",
            current_variables,
            "CHANGES:",
            changes
        )

          # Current state becomes previous state
        previous_variables = current_variables.copy()

        # execution_history.append(record)

        # print(record)

    return tracer


def run_tracer(filename):

    global TARGET_FILE

    TARGET_FILE = os.path.abspath(filename)

    with open(TARGET_FILE, "r") as file:
        code = compile(
            file.read(),
            TARGET_FILE,
            "exec"
        )

    sys.settrace(tracer)

    try:
        exec(code, {})
    finally:
        sys.settrace(None)


if __name__ == "__main__":
    run_tracer("scripts/basic.py")