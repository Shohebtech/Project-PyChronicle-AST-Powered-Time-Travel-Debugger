import sys
import os

step = 0
TARGET_FILE = None
execution_history = []


def tracer(frame, event, arg):
    global step

    # Trace only target Python file
    if frame.f_code.co_filename != TARGET_FILE:
        return tracer

    if event == "line":

        step += 1

        #these will remove the unecessary built-in variales
        variables = {
            key: value
            for key, value in frame.f_locals.items()
            if key != "__builtins__"
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

        execution_history.append(record)

        print(record)

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