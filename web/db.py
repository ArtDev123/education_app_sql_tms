"""Доступ к БД и репозиториям в контексте Flask-запроса."""

from flask import g

from database.connection import Database
from database.schemas import init_schema
from repositories.directions import DirectionRepository


def init_db() -> None:
    """Открыть соединение с БД для текущего запроса."""
    if "db" not in g:
        g.db = Database()
        g.db.connect()
        init_schema(g.db)


def close_db(exc: BaseException | None = None) -> None:
    """Закрыть соединение с БД."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def direction_repo() -> DirectionRepository:
    return DirectionRepository(g.db)
