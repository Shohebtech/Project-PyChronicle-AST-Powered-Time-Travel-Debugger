import ast
import json
import sqlite3
from typing import Any


class HistoryStore:
    """
    Adapter between the Textual UI and SQLite.

    Expected SQLite table:

        execution_states(
            id INTEGER PRIMARY KEY,
            position INTEGER,
            line_number INTEGER,
            variable_name TEXT,
            serialized_value TEXT
        )

    If Member 3 uses a different schema, only this adapter needs to change.
    The Textual UI does not need to know the database details.
    """

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path

    def get_history(self) -> list[dict[str, Any]]:
        if not self.db_path:
            return []

        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row

            rows = conn.execute(
                """
                SELECT position, line_number, variable_name, serialized_value
                FROM execution_states
                ORDER BY position ASC, id ASC
                """
            ).fetchall()
            conn.close()
        except (sqlite3.Error, OSError):
            return []

        points: dict[int, dict[str, Any]] = {}

        for row in rows:
            pos = int(row["position"])
            point = points.setdefault(
                pos,
                {"position": pos, "line": int(row["line_number"]), "state": {}},
            )

            point["line"] = int(row["line_number"])
            point["state"][row["variable_name"]] = self.deserialize(
                row["serialized_value"]
            )

        return list(points.values())

    @staticmethod
    def deserialize(value: str) -> Any:
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    def sample_history(self) -> list[dict[str, Any]]:
        """Sample data lets Member 4 develop the TUI before SQLite is connected."""
        return [
            {"position": 0, "line": 1, "state": {"total": 0}},
            {"position": 1, "line": 2, "state": {"total": 0, "i": 1}},
            {"position": 2, "line": 3, "state": {"total": 1, "i": 1}},
            {"position": 3, "line": 2, "state": {"total": 1, "i": 2}},
            {"position": 4, "line": 3, "state": {"total": 3, "i": 2}},
            {"position": 5, "line": 2, "state": {"total": 3, "i": 3}},
            {"position": 6, "line": 3, "state": {"total": 6, "i": 3}},
            {"position": 7, "line": 2, "state": {"total": 6, "i": 4}},
            {"position": 8, "line": 3, "state": {"total": 10, "i": 4}},
            {"position": 9, "line": 2, "state": {"total": 10, "i": 5}},
            {"position": 10, "line": 3, "state": {"total": 15, "i": 5}},
            {"position": 11, "line": 4, "state": {"total": 15, "i": 5}},
        ]
