"""Доступ к БД и репозиториям в контексте Flask-запроса."""

from flask import g

from database.connection import Database
from database.schemas import init_schema
from repositories.directions import DirectionRepository
from repositories.teachers import TeacherRepository
from repositories.courses import CourseRepository
from repositories.students import StudentRepository
from repositories.results import ResultRepository
from database.session import SessionLocal
from sqlalchemy.orm import Session


def init_db() -> None:
    """Открыть соединение с БД для текущего запроса."""
    if "db" not in g:
        g.db = Database()
        g.db.connect()
        g.session = SessionLocal()
        # init_schema(g.db)


def close_db(exc: BaseException | None = None) -> None:
    """Закрыть соединение с БД."""
    db = g.pop("db", None)
    session: Session = g.pop("session", None)
    if db is not None:
        db.close()
    if session is not None:
        session.close()


def direction_repo() -> DirectionRepository:
    return DirectionRepository(g.session)


def teacher_repo() -> TeacherRepository:
    return TeacherRepository(g.db)


def course_repo() -> CourseRepository:
    return CourseRepository(g.db)


def student_repo() -> StudentRepository:
    return StudentRepository(g.db)


def results_repo() -> ResultRepository:
    return ResultRepository(g.db)
