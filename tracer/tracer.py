import sys


def tracer(frame, event, arg):
    if event == "line":
        print(
            "LINE:",
            frame.f_lineno,
            "FUNCTION:",
            frame.f_code.co_name,
            "VARS:",
            frame.f_locals
        )

    return tracer


def run_tracer(filename):
    sys.settrace(tracer)

    with open(filename, "r") as file:
        code = compile(file.read(), filename, "exec")

    exec(code, {})

    sys.settrace(None)


if __name__ == "__main__":
    run_tracer("scripts/basic.py")