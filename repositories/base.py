"""Базовые утилиты для репозиториев."""

import sqlite3
from datetime import date
from typing import Optional


def require_lastrowid(cursor: sqlite3.Cursor) -> int:
    """Вернуть ID последней вставленной строки."""
    row_id = cursor.lastrowid
    if row_id is None:
        raise RuntimeError("INSERT did not return a row id")
    return row_id


def matches_partial(text: str, pattern: str) -> bool:
    """Проверить частичное совпадение без учёта регистра (включая кириллицу)."""
    return pattern.casefold() in text.casefold()


def parse_date(value: Optional[str]) -> Optional[date]:
    """Преобразовать строку ISO-даты в объект date."""
    if not value:
        return None
    return date.fromisoformat(value)


def format_date(value: Optional[date]) -> Optional[str]:
    """Преобразовать date в строку ISO."""
    if value is None:
        return None
    return value.isoformat()
