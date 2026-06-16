"""Диспетчер меню студентов."""

from cli.base import CrudDispatcher
from cli.helpers import pause, read_date, read_input, read_int
from models.entities import Student
from repositories.students import StudentRepository


class StudentDispatcher(CrudDispatcher):
    """Консольное меню студентов."""

    def __init__(self, repo: StudentRepository) -> None:
        self._repo = repo

    @property
    def _title(self) -> str:
        return "Студенты"

    def _add(self) -> None:
        first_name = read_input("Имя: ")
        last_name = read_input("Фамилия: ")
        direction_id = read_int("ID направления: ")
        if direction_id is None:
            return
        email = read_input("Email: ", required=False)
        enrollment_date = read_date("Дата зачисления")
        try:
            student_id = self._repo.add(
                Student(
                    id=None,
                    first_name=first_name,
                    last_name=last_name,
                    direction_id=direction_id,
                    email=email,
                    enrollment_date=enrollment_date,
                )
            )
        except ValueError as e:
            print(e)
            pause()
            return
        print(f"Студент добавлен (id={student_id}).")
        pause()

    def _list_all(self) -> None:
        items = self._repo.get_all()
        if not items:
            print("Студент не найден")
        for item in items:
            print(
                f"[{item.id}], {item.first_name}, {item.last_name}, "
                f"{item.direction_id}, {item.email}, {item.enrollment_date}"
            )
        pause()

    def _edit(self) -> None:
        student_id = read_int("ID студента: ")
        if student_id is None:
            return

        item = self._repo.get_by_id(student_id)

        if item is None:
            print("Студент не найден.")
            pause()
            return

        first_name = (
            read_input(f"Имя [{item.first_name}]: ", required=False) or item.first_name
        )
        last_name = (
            read_input(f"Фамилия [{item.last_name}]: ", required=False)
            or item.last_name
        )
        direction_id = (
            read_int(f"ID направления [{item.direction_id}]: ", required=False)
            or item.direction_id
        )
        email = read_input(f"Email [{item.email}]: ", required=False) or item.email
        enrollment_date = read_date("Дата зачисления") or item.enrollment_date

        try:
            updated = self._repo.update(
                Student(
                    id=student_id,
                    first_name=first_name,
                    last_name=last_name,
                    direction_id=direction_id,
                    email=email,
                    enrollment_date=enrollment_date,
                )
            )
        except ValueError as exc:
            print(exc)
            pause()
            return

        if updated:
            print("Студент обновлён.")
        else:
            print("Не удалось обновить.")
        pause()

    def _delete(self) -> None:
        student_id = read_int("ID студента: ")
        if student_id is None:
            return
        if self._repo.delete(student_id):
            print("Студен удален.")
        else:
            print("Студент не найден.")
        pause()
