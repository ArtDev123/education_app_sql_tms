import sqlite3
from typing import Any, cast
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "portal.db"


class Database:
    """Обёртка над sqlite3 с поддержкой контекстного менеджера."""

    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self._connection is not None:
            if exc_type is None:
                self._connection.commit()

            self.close()

    def execute(
        self,
        query: str,
        params: tuple[Any, ...] = (),
    ) -> sqlite3.Cursor:
        """Выполнить SQL-запрос."""
        cursor = self.connect().execute(query, params)
        self.connect().commit()
        return cursor

    def fetchone(
        self,
        query: str,
        params: tuple[Any, ...] = (),
    ) -> sqlite3.Row | None:
        """Выполнить запрос и вернуть одну строку."""
        row = self.connect().execute(query, params).fetchone()
        return cast(sqlite3.Row | None, row)

    def fetchall(
        self,
        query: str,
        params: tuple[Any, ...] = (),
    ) -> list[sqlite3.Row]:
        """Выполнить запрос и вернуть все строки."""
        return self.connect().execute(query, params).fetchall()

    def __enter__(self) -> "Database":
        self.connect()
        return self
