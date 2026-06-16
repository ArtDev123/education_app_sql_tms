"""Диспетчер меню преподавателей."""

from cli.base import CrudDispatcher
from cli.helpers import pause, read_input, read_int
from models.entities import Teacher
from repositories.teachers import TeacherRepository


class TeacherDispatcher(CrudDispatcher):
    """Консольное меню преподавателей."""

    def __init__(self, repo: TeacherRepository) -> None:
        self._repo = repo

    @property
    def _title(self) -> str:
        return "Учителя"

    def _add(self) -> None:
        first_name = read_input("Имя: ")
        last_name = read_input("Фамилия: ")
        email = read_input("Email: ", required=False)
        phone = read_input("Phone: ", required=False)
        teacher_id = self._repo.add(
            Teacher(
                id=None,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )
        )
        print(f"Учитель добавлен (id={teacher_id}).")
        pause()

    def _list_all(self) -> None:
        items = self._repo.get_all()
        if not items:
            print("Учителя не найдены.")
        for item in items:
            print(
                f"[{item.id}], {item.first_name}, {item.last_name}, "
                f"{item.email}, {item.phone}"
            )
        pause()

    def _edit(self) -> None:
        teacher_id = read_int("ID учителя: ")
        if teacher_id is None:
            return
        item = self._repo.get_by_id(teacher_id)
        if item is None:
            print("Учитель не найден.")
            pause()
            return
        first_name = (
            read_input(f"Имя [{item.first_name}]: ", required=False) or item.first_name
        )
        last_name = (
            read_input(f"Фамилия [{item.last_name}]: ", required=False)
            or item.last_name
        )
        email = read_input(f"Email [{item.email}]: ", required=False) or item.email
        phone = read_input(f"Телефон [{item.phone}]: ", required=False) or item.phone

        if self._repo.update(
            teacher=Teacher(
                id=teacher_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )
        ):
            print("Учитель обновлен.")
        else:
            print("Учитель не найден.")
        pause()

    def _delete(self) -> None:
        teacher_id = read_int("ID учителя: ")
        if teacher_id is None:
            return
        if self._repo.delete(teacher_id):
            print("Учитель удален.")
        else:
            print("Учитель не найден.")
        pause()
