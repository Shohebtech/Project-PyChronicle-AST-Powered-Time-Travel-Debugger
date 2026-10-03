# PyChronicle: AST-Powered Time-Travel Debugger

PyChronicle is a terminal-based Python developer tool that records the complete
execution history of a Python program and lets you move backward and forward
through that history, instead of only stepping forward like a normal debugger.

This repository contains PyChronicle's four modules, built by a team of four.

## This Module: AST Rewriter + CLI (Module 1)

This module is responsible for:
- Reading and understanding a target Python script (via its AST)
- Detecting every variable assignment and mutation in it
- Rewriting a copy of the script so it reports on itself when run
- Providing the `pychronicle run <script>` command that ties the pipeline together

**The original script is never modified.** A separate, transformed copy is
generated in `output/` and executed instead.

## Setup

Requires Python 3.8+.

From the project root, install the CLI in editable mode:

```bash
pip install -e .
```

This registers the `pychronicle` command. If it isn't recognized after
installing, you can always run it as `python -m pychronicle` instead.

## Usage

```bash
pychronicle run tests/sample_scripts/sample1.py
```

This will:
1. Validate the given file
2. Parse it into an AST
3. Insert tracking calls after every assignment/mutation found
4. Write the transformed version to `output/`
5. Run the transformed version and print its tracked output

Example output:
```
Reading: tests/sample_scripts/sample1.py
Parsing and transforming...
Transformed file written to: output/sample1_transformed.py
Running transformed program...
[TRACK] Line 1: x = 10
[TRACK] Line 2: y = 20
...
```

You can also run the detector on its own, to see assignment detection
without transformation:

```bash
python -m ast_rewriter.assignment_detector
```

## What's Supported

Assignment detection and transformation currently cover:
- Simple assignments (`x = 10`)
- Multiple-target assignments (`a = b = 5`)
- Tuple/list unpacking (`x, y = 1, 2`)
- Attribute and subscript assignments (`obj.x = 5`, `arr[0] = 5`)
- Assignments inside `if` / `elif` / `else`
- Assignments inside `for` / `while` loops
- Assignments inside functions
- Assignments inside `try` / `except` / `else` / `finally`
- Mutations (`x += 5`, etc.)

## Architecture

```
file path -> AST tree -> transformed AST tree -> output .py file -> executed
  (CLI)      (parser)       (transformer)         (transformer)      (CLI)
```

The parser and transformer never touch the original file — a fresh AST is
built in memory and only the transformed copy is written to disk.

## Current Limitations

- `track()` (the function injected into transformed scripts) is currently a
  stub that prints to the console. In the full project, it will hand data
  off to the Execution Tracer module instead.
- Classes/methods are detected but not yet transformed (their assignments
  aren't tracked yet).
- Integration with the Tracer, SQLite Storage, and TUI modules is not yet
  implemented — that's the next phase of development.

## Project Structure

```
ast_rewriter/       AST parsing, detection, and transformation logic
pychronicle/         CLI entry point (pychronicle run <script>)
tests/sample_scripts/  Sample Python files used for testing
output/              Auto-generated transformed files (not tracked in git)
```