# PyChronicle

PyChronicle is an AST-assisted time-travel debugger with a SQLite-backed execution history and a Textual terminal UI.

## Install

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

PyChronicle requires Python 3.10 or newer.

## Run

Run with sample data only:

```bash
python app.py --source sample_program.py
```

Run the target through the tracer, write a fresh SQLite history, and open the UI on that history:

```bash
python app.py --db pychronicle.db --source sample_program.py
```

Each run replaces the existing execution history in the selected database.

## Controls

- Left/Right Arrow: previous or next execution point
- Home/End: first or last execution point
- Slider: jump to an execution point
- Watch: add a variable to the watch list
- Select a watched variable: remove it
- q: quit

## Architecture

```text
Target Python script
        |
        v
Execution Tracer
        |
        v
SQLite Storage
        |
        v
Textual TUI
```

The AST rewriter and assignment detector are also available for static analysis and transformed-script experiments through the `pychronicle run` command.
