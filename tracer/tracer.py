import sys
import os

previous_variables = {}
execution_history = []
step_counter = 0
TARGET_FILE = None


def tracer(frame, event, arg):

    global step_counter

    
    if frame.f_code.co_filename != TARGET_FILE:
        return tracer

    function_name = frame.f_code.co_name

   
    step_counter += 1


    if event == "call":

        record = {
            "step": step_counter,
            "event": "CALL",
            "line": frame.f_lineno,
            "function": function_name
        }

        execution_history.append(record)

        print(
            "STEP:", step_counter,
            "CALL:",
            function_name,
            "LINE:",
            frame.f_lineno
        )

   
    elif event == "line":

       
        current_variables = {
            key: value
            for key, value in frame.f_locals.items()
            if key != "__builtins__"
        }

    
        previous = previous_variables.get(frame, {})

        changes = {}

       
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

   
        for key in previous:

            if key not in current_variables:

                changes[key] = {
                    "type": "REMOVED",
                    "old": previous[key]
                }

        record = {
            "step": step_counter,
            "event": "LINE",
            "line": frame.f_lineno,
            "function": function_name,
            "variables": current_variables.copy(),
            "changes": changes
        }

        execution_history.append(record)

        print(
            "STEP:", step_counter,
            "LINE:",
            frame.f_lineno,
            "FUNCTION:",
            function_name,
            "VARS:",
            current_variables,
            "CHANGES:",
            changes
        )

        previous_variables[frame] = current_variables.copy()

    elif event == "return":

        record = {
            "step": step_counter,
            "event": "RETURN",
            "line": frame.f_lineno,
            "function": function_name,
            "return_value": arg
        }

        execution_history.append(record)

        print(
            "STEP:", step_counter,
            "RETURN:",
            function_name,
            "VALUE:",
            arg
        )

    elif event == "exception":

        exception_type, exception_value, traceback = arg

        record = {
            "step": step_counter,
            "event": "EXCEPTION",
            "line": frame.f_lineno,
            "function": function_name,
            "exception_type": exception_type.__name__,
            "message": str(exception_value)
        }

        execution_history.append(record)

        print(
            "STEP:", step_counter,
            "EXCEPTION:",
            exception_type.__name__,
            "MESSAGE:",
            str(exception_value),
            "LINE:",
            frame.f_lineno,
            "FUNCTION:",
            function_name
        )

    return tracer


def run_tracer(filename):

    global TARGET_FILE
    global step_counter
    global execution_history
    global previous_variables


    step_counter = 0
    execution_history = []
    previous_variables = {}


    TARGET_FILE = os.path.abspath(filename)


    with open(TARGET_FILE, "r") as file:
        code = compile(
            file.read(),
            TARGET_FILE,
            "exec"
        )

    # Start tracing
    sys.settrace(tracer)

    try:
        exec(code, {})

    finally:
        # stop tracing
        sys.settrace(None)


if __name__ == "__main__":

    run_tracer("scripts/complex_test.py")

    print("\n========== EXECUTION HISTORY ==========\n")

    for record in execution_history:
        print(record)

