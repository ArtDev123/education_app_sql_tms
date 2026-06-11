"""Репозиторий учебных направлений."""

from typing import Optional

from database.connection import Database
from models.entities import Teacher
from repositories.base import require_lastrowid
from repositories.interfaces import ITeacherRepository


class TeacherRepository(ITeacherRepository):
    """CRUD-операции для направлений."""

    def __init__(self, db: Database) -> None:
        self._db = db

    def add(self, teacher: Teacher) -> int:
        """Добавить направление."""
        cursor = self._db.execute(
            "INSERT INTO teachers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
            (teacher.first_name, teacher.last_name, teacher.email, teacher.phone),
        )
        return require_lastrowid(cursor)

    def get_by_id(self, teacher_id: int) -> Optional[Teacher]:
        """Получить направление по ID."""
        row = self._db.fetchone(
            "SELECT id, first_name, last_name, email, phone FROM teachers WHERE id = ?",
            (teacher_id,),
        )
        if row is None:
            return None
        return self._row_to_teacher(row)

    def get_all(self) -> list[Teacher]:
        """Получить все направления."""
        rows = self._db.fetchall(
            "SELECT id, first_name, last_name, email, phone FROM teachers ORDER BY id",
        )
        return [self._row_to_teacher(row) for row in rows]

    def update(self, teacher: Teacher) -> bool:
        """Обновить направление."""
        if teacher.id is None:
            return False
        cursor = self._db.execute(
            "UPDATE teachers SET first_name = ?, last_name = ?, email = ?, phone = ? WHERE id = ?",
            (
                teacher.first_name,
                teacher.last_name,
                teacher.email,
                teacher.phone,
                teacher.id,
            ),
        )
        return cursor.rowcount > 0

    def delete(self, teacher_id: int) -> bool:
        """Удалить направление."""
        cursor = self._db.execute(
            "DELETE FROM teachers WHERE id = ?",
            (teacher_id,),
        )
        return cursor.rowcount > 0

    @staticmethod
    def _row_to_teacher(row: object) -> Teacher:
        """Преобразовать строку БД в модель Teacher."""
        return Teacher(
            id=row["id"],  # type: ignore[index]
            first_name=row["first_name"],  # type: ignore[index]
            last_name=row["last_name"],  # type: ignore[index]
            email=row["email"],  # type: ignore[index]
            phone=row["phone"],  # type: ignore[index]
        )


if __name__ == "__main__":
    with Database() as db:
        repo = TeacherRepository(db=db)

        # teacher_1 = Teacher(
        #     id=None,
        #     first_name="Artem",
        #     last_name="aaa",
        #     email="email@gmail.com",
        #     phone=123,
        # )

        # repo.add(teacher_1)

        # teacher_update = Teacher(
        #     id=1,
        #     first_name="Artem_2",
        #     last_name="asdlkfja",
        # )
        # repo.update(teacher_update)
# if __name__ == "__main__":
#     with Database() as db:
#         repo = DirectionRepository(db)
#         dir1 = Direction(id = None, name = "прога")
#         repo.add(dir1)
