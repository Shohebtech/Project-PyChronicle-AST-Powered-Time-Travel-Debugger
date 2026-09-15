# PyChronicle — Textual TUI

This is the Member 4 implementation for the PyChronicle project.

The project plan requires the Textual TUI to provide:

- terminal dashboard/layout
- target Python source-code display
- current historical line highlighting
- timeline/slider navigation
- backward and forward history navigation
- variable/state display
- SQLite connection
- Watch Variables
- demo-ready interface

The TUI can first run with sample data, then connect to Member 3's SQLite layer.

## 1. Install

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

## 2. Run the UI with sample data

```bash
python app.py --source sample_program.py
```

This demonstrates the complete UI without needing the tracer or SQLite database.

## 3. Controls

- Left Arrow: previous execution point
- Right Arrow: next execution point
- Home: first point
- End: last point
- Mouse/keyboard: move the timeline slider
- Enter a variable name and press Watch
- Click a watched variable to remove it
- q: quit

## 4. SQLite integration

Run:

```bash
python app.py --db pychronicle.db --source sample_program.py
```

The adapter expects:

```sql
CREATE TABLE execution_states (
    id INTEGER PRIMARY KEY,
    position INTEGER NOT NULL,
    line_number INTEGER NOT NULL,
    variable_name TEXT NOT NULL,
    serialized_value TEXT
);
```

If Member 3's actual schema has different names, modify only `storage_adapter.py`.

## 5. Integration contract with the team

The TUI should receive historical records logically equivalent to:

```python
[
    {
        "position": 0,
        "line": 1,
        "state": {"total": 0}
    },
    {
        "position": 1,
        "line": 2,
        "state": {"total": 0, "i": 1}
    }
]
```

The tracer/storage modules may use any internal representation, but the UI needs:

- execution position
- current source line
- variable name
- variable value

## 6. Final team pipeline

```text
Target Python script
        |
        v
AST Rewriter
        |
        v
Execution Tracer
(sys.settrace)
        |
        v
SQLite Storage
        |
        v
Textual TUI
        |
        v
Developer navigates execution history
```

The project plan explicitly says the four modules must eventually work as one continuous pipeline and not as isolated pieces.
