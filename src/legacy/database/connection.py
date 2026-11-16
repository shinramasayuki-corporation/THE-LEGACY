"""SQLite database initialization and connections."""

import os
import sqlite3
from pathlib import Path

DEFAULT_DATABASE_PATH = Path("data/legacy.db")
SCHEMA_PATH = Path(__file__).with_name("schema.sql")

def connect_database(database_path: str | Path | None = None) -> sqlite3.Connection:
    path = Path(
        database_path
        or os.getenv("DATABASE_PATH", str(DEFAULT_DATABASE_PATH))
    )
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialize_database(database_path: str | Path | None = None) -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with connect_database(database_path) as connection:
        connection.executescript(schema)
        connection.executemany(
            """
            INSERT OR IGNORE INTO roles (role_key, label, description)
            VALUES (?, ?, ?)
            """,
            [
                ("member", "Member", "Standard community member."),
                ("contributor", "Contributor", "Community contributor."),
                ("moderator", "Moderator", "Community moderation role."),
                ("administrator", "Administrator", "Administrative role."),
                ("system", "System", "Internal system role."),
            ],
        )
