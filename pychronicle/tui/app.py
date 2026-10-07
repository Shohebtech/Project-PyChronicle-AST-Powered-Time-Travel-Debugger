from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Horizontal, Vertical


class PyChronicleApp(App):

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():

            with Vertical():
                yield Static("Python Source")
                yield Static(
                    "1  x = 10\n"
                    "2  y = 20\n"
                    "3  total = x + y\n"
                    "4  print(total)"
                )

            with Vertical():
                yield Static("Variables")
                yield Static(
                    "x = 10\n"
                    "y = 20\n"
                    "total = 30"
                )

        yield Footer()


if __name__ == "__main__":
    PyChronicleApp().run()