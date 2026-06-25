"""Репозиторий курсов"""

from typing import Optional

from database.connection import Database
from models.entities import Course
from repositories.base import require_lastrowid
from repositories.interfaces import ICourseRepository
from repositories.directions import DirectionRepository
from repositories.teachers import TeacherRepository


class CourseRepository(ICourseRepository):
    """CRUD-операции для курсов."""

    def __init__(self, db: Database) -> None:
        self._db = db
        self._direction_repo = DirectionRepository(db)
        self._teacher_repo = TeacherRepository(db)

    def add(self, course: Course) -> int:
        """Добавить курс"""
        if self._direction_repo.get_by_id(direction_id=course.direction_id) is None:
            raise ValueError(f"Направление с Id: {course.direction_id} - не существует")
        if course.teacher_id is not None:
            if self._teacher_repo.get_by_id(teacher_id=course.teacher_id) is None:
                raise ValueError(f"Учитель с Id: {course.teacher_id} - не существует")
        cursor = self._db.execute(
            "INSERT INTO courses (name, direction_id, teacher_id) VALUES (?, ?, ?)",
            (course.name, course.direction_id, course.teacher_id),
        )
        return require_lastrowid(cursor)

    def get_by_id(self, course_id: int) -> Optional[Course]:
        """Получить курс по ID."""
        row = self._db.fetchone(
            "SELECT id, name, direction_id, teacher_id FROM courses WHERE id = ?",
            (course_id,),
        )
        if row is None:
            return None
        return self._row_to_course(row)

    def get_all(self) -> list[Course]:
        """Получить все курсы."""
        rows = self._db.fetchall(
            "SELECT id, name, teacher_id, direction_id FROM courses ORDER BY name",
        )
        return [self._row_to_course(row) for row in rows]

    def update(self, course: Course) -> bool:
        """Обновить курс."""
        if course.id is None:
            return False
        if self._direction_repo.get_by_id(direction_id=course.direction_id) is None:
            raise ValueError(f"Направление с Id: {course.direction_id} - не существует")
        if course.teacher_id is not None:
            if self._teacher_repo.get_by_id(teacher_id=course.teacher_id) is None:
                raise ValueError(f"Учитель с Id: {course.teacher_id} - не существует")
        cursor = self._db.execute(
            "UPDATE courses SET name = ?, teacher_id = ?, direction_id = ? WHERE id = ?",
            (course.name, course.teacher_id, course.direction_id, course.id),
        )
        return cursor.rowcount > 0

    def delete(self, course_id: int) -> bool:
        """Удалить курс."""
        cursor = self._db.execute(
            "DELETE FROM courses WHERE id = ?",
            (course_id,),
        )
        return cursor.rowcount > 0

    @staticmethod
    def _row_to_course(row: object) -> Course:
        """Преобразовать строку БД в модель Teacher."""
        return Course(
            id=row["id"],  # type: ignore[index]
            name=row["name"],  # type: ignore[index]
            direction_id=row["direction_id"],  # type: ignore[index]
            teacher_id=row["teacher_id"],  # type: ignore[index]
        )


if __name__ == "__main__":
    with Database() as db:
        repo = CourseRepository(db)
        dir1 = Course(id=None, name="прога", direction_id=1, teacher_id=1)
        repo.add(dir1)
