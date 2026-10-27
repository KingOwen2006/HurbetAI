"""Private, local conversation storage."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def initialise(database: Path) -> None:
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                created_at TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL
            )"""
        )


def save_message(database: Path, role: str, content: str) -> None:
    with sqlite3.connect(database) as connection:
        connection.execute(
            "INSERT INTO messages(created_at, role, content) VALUES (?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), role, content),
        )


def load_messages(database: Path, limit: int = 100) -> list[tuple[str, str]]:
    with sqlite3.connect(database) as connection:
        rows = connection.execute(
            "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return list(reversed(rows))
