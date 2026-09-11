import sys


def tracer(frame, event, arg):
    if event == "line":


        #these will remove the unecessary built-in variales
        variables = {
            key: value
            for key, value in frame.f_locals.items()
            if key != "__builtins__"
        }

        print(
            "LINE:",
            frame.f_lineno,
            "FUNCTION:",
            frame.f_code.co_name,
            # "VARS:",
            # frame.f_locals
            "VARS:",
            variables
        )

    return tracer


def run_tracer(filename):

    with open(filename, "r") as file:
        code = compile(file.read(), filename, "exec")

    sys.settrace(tracer)

    try:
        exec(code, {})
    finally:
        sys.settrace(None)


if __name__ == "__main__":
    run_tracer("scripts/basic.py")