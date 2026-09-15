from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Static, TextArea, Label, Slider, Input, Button, ListView, ListItem
from textual.reactive import reactive
from rich.text import Text
from rich.syntax import Syntax

from storage_adapter import HistoryStore


class CodeView(Static):
    """Source-code pane with the current historical line highlighted."""

    current_line = reactive(1)

    def __init__(self, source: str = "", **kwargs):
        super().__init__(**kwargs)
        self.source = source

    def set_source(self, source: str) -> None:
        self.source = source
        self.refresh()

    def watch_current_line(self, line: int) -> None:
        self.refresh()

    def render(self):
        if not self.source:
            return Text("No source code loaded.", style="dim")

        lines = self.source.splitlines()
        output = Text()

        for number, line in enumerate(lines, start=1):
            prefix = f"{number:4}  "
            if number == self.current_line:
                output.append(prefix, style="bold reverse")
                output.append(line if line else " ", style="bold reverse")
            else:
                output.append(prefix, style="dim")
                output.append(line)
            output.append("\n")

        return output


class StatePanel(Static):
    """Shows variables for the selected history position."""

    def set_state(self, state: dict, watched: set[str]) -> None:
        output = Text()
        if not state:
            output.append("No variable state available.", style="dim")
            self.update(output)
            return

        for name, value in sorted(state.items()):
            marker = " ★" if name in watched else ""
            output.append(f"{name}{marker}", style="bold cyan" if name in watched else "bold")
            output.append(f" = {value}\n")

        self.update(output)


class Timeline(Static):
    """Small textual summary of the selected timeline point."""

    def set_position(self, position: int, total: int, line: int) -> None:
        self.update(
            f"Execution point: {position + 1}/{max(total, 1)}   |   "
            f"Current line: {line}"
        )


class PyChronicleTUI(App):
    TITLE = "PyChronicle — Time-Travel Debugger"
    SUB_TITLE = "Textual TUI"

    CSS = """
    Screen {
        layout: vertical;
    }

    #main {
        height: 1fr;
    }

    #left {
        width: 58%;
        border: solid $primary;
        padding: 0 1;
    }

    #right {
        width: 42%;
    }

    #state_box, #watch_box {
        height: 1fr;
        border: solid $secondary;
        margin: 0 0 1 1;
        padding: 1;
    }

    #timeline_box {
        height: 7;
        border: solid $accent;
        padding: 0 1;
    }

    #code_title, #state_title, #watch_title {
        text-style: bold;
        margin-bottom: 1;
    }

    #code {
        height: 1fr;
        overflow-y: auto;
    }

    #slider {
        width: 1fr;
    }

    #watch_input {
        margin-bottom: 1;
    }

    #watch_list {
        height: 1fr;
    }

    .hint {
        color: $text-muted;
    }

    Button {
        margin-left: 1;
    }
    """

    BINDINGS = [
        ("left", "previous_point", "Previous"),
        ("right", "next_point", "Next"),
        ("home", "first_point", "First"),
        ("end", "last_point", "Last"),
        ("q", "quit", "Quit"),
    ]

    position = reactive(0)
    watched: set[str] = set()

    def __init__(self, db_path: str | None = None, source_path: str | None = None):
        super().__init__()
        self.db_path = db_path
        self.source_path = source_path
        self.store = HistoryStore(db_path) if db_path else HistoryStore()
        self.source = ""

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="main"):
            with Vertical(id="left"):
                yield Label("SOURCE CODE", id="code_title")
                yield CodeView(id="code")
                with Container(id="timeline_box"):
                    yield Timeline(id="timeline")
                    yield Slider(0, 0, value=0, id="slider")
                    yield Label(
                        "←/→ move through execution   Home/End jump   "
                        "Watch variables on the right",
                        classes="hint",
                    )

            with Vertical(id="right"):
                with Container(id="state_box"):
                    yield Label("VARIABLE STATE", id="state_title")
                    yield StatePanel(id="state")

                with Container(id="watch_box"):
                    yield Label("WATCH VARIABLES", id="watch_title")
                    with Horizontal():
                        yield Input(
                            placeholder="Variable name (e.g. total)",
                            id="watch_input",
                        )
                        yield Button("Watch", id="watch_button")
                    yield ListView(id="watch_list")

        yield Footer()

    def on_mount(self) -> None:
        self.load_data()

    def load_data(self) -> None:
        if self.source_path:
            try:
                self.source = open(self.source_path, "r", encoding="utf-8").read()
            except OSError as exc:
                self.notify(f"Could not read source: {exc}", severity="error")
        else:
            self.source = (
                "total = 0\n"
                "for i in range(1, 6):\n"
                "    total += i\n"
                "print(total)\n"
            )

        history = self.store.get_history()

        if not history:
            history = self.store.sample_history()

        self.history = history
        slider = self.query_one("#slider", Slider)
        slider.high = max(len(self.history) - 1, 0)
        slider.value = 0

        self.query_one("#code", CodeView).set_source(self.source)
        self.refresh_position()

    def refresh_position(self) -> None:
        if not self.history:
            return

        point = self.history[self.position]
        line = int(point["line"])
        state = point.get("state", {})

        self.query_one("#code", CodeView).current_line = line
        self.query_one("#state", StatePanel).set_state(state, self.watched)
        self.query_one("#timeline", Timeline).set_position(
            self.position, len(self.history), line
        )

    def set_position(self, position: int) -> None:
        if not self.history:
            return
        position = max(0, min(position, len(self.history) - 1))
        self.position = position
        self.query_one("#slider", Slider).value = position
        self.refresh_position()

    def on_slider_changed(self, event: Slider.Changed) -> None:
        if event.slider.id == "slider":
            self.position = int(event.value)
            self.refresh_position()

    def action_previous_point(self) -> None:
        self.set_position(self.position - 1)

    def action_next_point(self) -> None:
        self.set_position(self.position + 1)

    def action_first_point(self) -> None:
        self.set_position(0)

    def action_last_point(self) -> None:
        self.set_position(len(self.history) - 1)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "watch_button":
            return

        name = self.query_one("#watch_input", Input).value.strip()
        if not name:
            self.notify("Enter a variable name.", severity="warning")
            return

        self.watched.add(name)
        self.query_one("#watch_input", Input).value = ""
        self.update_watch_list()
        self.refresh_position()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id and event.item.id.startswith("watch-"):
            name = event.item.id.removeprefix("watch-")
            self.watched.discard(name)
            self.update_watch_list()
            self.refresh_position()

    def update_watch_list(self) -> None:
        watch_list = self.query_one("#watch_list", ListView)
        watch_list.clear()

        for name in sorted(self.watched):
            watch_list.append(ListItem(Label(f"★ {name}"), id=f"watch-{name}"))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PyChronicle Textual TUI")
    parser.add_argument("--db", help="SQLite database produced by the storage module")
    parser.add_argument("--source", help="Target Python source file")
    args = parser.parse_args()

    PyChronicleTUI(db_path=args.db, source_path=args.source).run()
