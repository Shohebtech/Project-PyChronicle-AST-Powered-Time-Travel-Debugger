import sys
import os

# Stores previous variables 
previous_variables = {}

# Path of the Python program 
TARGET_FILE = None


def tracer(frame, event, arg):

    # Trace only the target Python file
    if frame.f_code.co_filename != TARGET_FILE:
        return tracer

    function_name = frame.f_code.co_name

   
    if event == "call":

        print(
            "CALL:",
            function_name,
            "LINE:",
            frame.f_lineno
        )

    
    elif event == "line":

        # Capture current variables
        current_variables = {
            key: value
            for key, value in frame.f_locals.items()
            if key != "__builtins__"
        }

        # Get previous state of THIS frame
        previous = previous_variables.get(frame, {})

        changes = {}

        # Check new and modified variables
        for key, value in current_variables.items():

            if key not in previous:

                changes[key] = {
                    "type": "NEW",
                    "value": value
                }

            elif previous[key] != value:

                changes[key] = {
                    "type": "MODIFIED",
                    "old": previous[key],
                    "new": value
                }

        # Check removed variables
        for key in previous:

            if key not in current_variables:

                changes[key] = {
                    "type": "REMOVED",
                    "old": previous[key]
                }

        print(
            "LINE:",
            frame.f_lineno,
            "FUNCTION:",
            function_name,
            "VARS:",
            current_variables,
            "CHANGES:",
            changes
        )

        # Save current state for this frame
        previous_variables[frame] = current_variables.copy()


    elif event == "return":

        print(
            "RETURN:",
            function_name,
            "VALUE:",
            arg
        )

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

    sys.settrace(tracer) # start tracing

    try:
        exec(code, {})
    finally:
        sys.settrace(None) # stop tracing


if __name__ == "__main__":
    run_tracer("scripts/function-script.py")

