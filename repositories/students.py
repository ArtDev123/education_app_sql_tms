"""Репозиторий учебных направлений."""

from typing import Optional

from database.connection import Database
from models.entities import Student
from repositories.base import require_lastrowid, format_date, parse_date
from repositories.interfaces import IStudentsRepository
from repositories.directions import DirectionRepository


class StudentRepository(IStudentsRepository):
    """Студенты."""

    def __init__(self, db: Database) -> None:
        self._db = db
        self._direction_repo = DirectionRepository(db)

    def add(self, student: Student) -> int:
        """Добавить студента."""
        if self._direction_repo.get_by_id(direction_id=student.direction_id) is None:
            raise ValueError(
                f"Направление с Id: {student.direction_id} - не существует"
            )
        cursor = self._db.execute(
            "INSERT INTO students (first_name, last_name, email, direction_id, enrollment_date) VALUES (?, ?, ?, ?, ?)",
            (
                student.first_name,
                student.last_name,
                student.email,
                student.direction_id,
                format_date(student.enrollment_date),
            ),
        )
        return require_lastrowid(cursor)

    def get_by_id(self, student_id: int) -> Optional[Student]:
        """Получить студенета по ID."""
        row = self._db.fetchone(
            "SELECT id, first_name, last_name, email, direction_id, enrollment_date FROM students WHERE id = ?",
            (student_id,),
        )
        if row is None:
            return None
        return self._row_to_student(row)

    def get_all(self) -> list[Student]:
        """Получить всех студентов."""
        rows = self._db.fetchall(
            "SELECT id, first_name, last_name, email, direction_id, enrollment_date FROM students ORDER BY id",
        )
        return [self._row_to_student(row) for row in rows]

    def update(self, student: Student) -> bool:
        """Обновить студента."""
        if student.id is None:
            return False
        if self._direction_repo.get_by_id(direction_id=student.direction_id) is None:
            raise ValueError(
                f"Направление с Id: {student.direction_id} - не существует"
            )
        cursor = self._db.execute(
            "UPDATE students SET first_name = ?, last_name = ?, email = ?, direction_id = ?, enrollment_date = ? WHERE id = ?",
            (
                student.first_name,
                student.last_name,
                student.email,
                student.direction_id,
                student.enrollment_date,
                student.id,
            ),
        )
        return cursor.rowcount > 0

    def delete(self, student_id: int) -> bool:
        """Удалить студента."""
        cursor = self._db.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,),
        )
        return cursor.rowcount > 0

    @staticmethod
    def _row_to_student(row: object) -> Student:
        """Преобразовать строку БД в модель Student."""
        return Student(
            id=row["id"],  # type: ignore[index]
            first_name=row["first_name"],  # type: ignore[index]
            last_name=row["last_name"],  # type: ignore[index]
            email=row["email"],  # type: ignore[index]
            direction_id=row["direction_id"],  # type: ignore[index]
            enrollment_date=parse_date(row["enrollment_date"]),  # type: ignore[index]
        )


if __name__ == "__main__":
    with Database() as db:
        repo = StudentRepository(db=db)
        from models.entities import Direction
        from datetime import date

        direction_repo = DirectionRepository(db)
        direction1 = Direction(id=None, name="Evgeni")
        direction_repo.add(direction1)

        student_1 = Student(
            id=None,
            first_name="Artem",
            last_name="aaa",
            email="email@gmail.com",
            direction_id=1,
            enrollment_date=date(year=1996, month=4, day=26),
        )

        repo.add(student_1)
        print(repo.get_by_id(1))

        # Student_update = Student(
        #     id=1,
        #     first_name="Artem_2",
        #     last_name="asdlkfja",
        # )
        # repo.update(Student_update)
# if __name__ == "__main__":
#     with Database() as db:
#         repo = DirectionRepository(db)
#         dir1 = Direction(id = None, name = "прога")
#         repo.add(dir1)
