"""Репозиторий оценок студентов."""

from typing import Optional

from database.connection import Database
from models.entities import StudentResult
from repositories.base import format_date, parse_date, require_lastrowid
from repositories.courses import CourseRepository
from repositories.interfaces import IResultRepository
from repositories.students import StudentRepository


class ResultRepository(IResultRepository):
    """CRUD-операции для оценок студентов."""

    def __init__(self, db: Database) -> None:
        self._db = db
        self._student_repo = StudentRepository(db)
        self._course_repo = CourseRepository(db)

    def add(self, result: StudentResult) -> int:
        """Добавить оценку."""
        self._validate(result)
        cursor = self._db.execute(
            "INSERT INTO student_results (student_id, course_id, grade, exam_date) "
            "VALUES (?, ?, ?, ?)",
            (
                result.student_id,
                result.course_id,
                result.grade,
                format_date(result.exam_date),
            ),
        )
        return require_lastrowid(cursor)

    def get_by_id(self, result_id: int) -> Optional[StudentResult]:
        """Получить оценку по ID."""
        row = self._db.fetchone(
            "SELECT id, student_id, course_id, grade, exam_date "
            "FROM student_results WHERE id = ?",
            (result_id,),
        )
        if row is None:
            return None
        return self._row_to_result(row)

    def get_all(self) -> list[StudentResult]:
        """Получить все оценки."""
        rows = self._db.fetchall(
            "SELECT id, student_id, course_id, grade, exam_date "
            "FROM student_results ORDER BY id",
        )
        return [self._row_to_result(row) for row in rows]

    def get_by_student(self, student_id: int) -> list[StudentResult]:
        """Получить оценки студента."""
        rows = self._db.fetchall(
            "SELECT id, student_id, course_id, grade, exam_date "
            "FROM student_results WHERE student_id = ? ORDER BY id",
            (student_id,),
        )
        return [self._row_to_result(row) for row in rows]

    def get_by_course(self, course_id: int) -> list[StudentResult]:
        """Получить оценки по курсу."""
        rows = self._db.fetchall(
            "SELECT id, student_id, course_id, grade, exam_date "
            "FROM student_results WHERE course_id = ? ORDER BY id",
            (course_id,),
        )
        return [self._row_to_result(row) for row in rows]

    def update(self, result: StudentResult) -> bool:
        """Обновить оценку."""
        if result.id is None:
            return False
        self._validate(result)
        cursor = self._db.execute(
            "UPDATE student_results SET student_id = ?, course_id = ?, grade = ?, "
            "exam_date = ? WHERE id = ?",
            (
                result.student_id,
                result.course_id,
                result.grade,
                format_date(result.exam_date),
                result.id,
            ),
        )
        return cursor.rowcount > 0

    def delete(self, result_id: int) -> bool:
        """Удалить оценку."""
        cursor = self._db.execute(
            "DELETE FROM student_results WHERE id = ?",
            (result_id,),
        )
        return cursor.rowcount > 0

    def _validate(self, result: StudentResult) -> None:
        """Проверить корректность оценки и внешних ключей."""
        if not 1 <= result.grade <= 5:
            raise ValueError("Оценка должна быть от 1 до 5")
        if self._student_repo.get_by_id(result.student_id) is None:
            raise ValueError(f"Студент с Id: {result.student_id} - не существует")
        if self._course_repo.get_by_id(result.course_id) is None:
            raise ValueError(f"Курс с Id: {result.course_id} - не существует")

    @staticmethod
    def _row_to_result(row: object) -> StudentResult:
        """Преобразовать строку БД в модель StudentResult."""
        return StudentResult(
            id=row["id"],  # type: ignore[index]
            student_id=row["student_id"],  # type: ignore[index]
            course_id=row["course_id"],  # type: ignore[index]
            grade=row["grade"],  # type: ignore[index]
            exam_date=parse_date(row["exam_date"]),  # type: ignore[index]
        )
