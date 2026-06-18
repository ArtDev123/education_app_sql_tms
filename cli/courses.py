"""Диспетчер меню направлений."""

from cli.base import CrudDispatcher
from cli.helpers import pause, read_input, read_int
from models.entities import Course
from repositories.courses import CourseRepository


class CourseDispatcher(CrudDispatcher):
    """Консольное меню курсов."""

    def __init__(self, repo: CourseRepository) -> None:
        self._repo = repo

    @property
    def _title(self) -> str:
        return "Курсы"

    def _add(self) -> None:
        name = read_input("Название: ")
        direction_id = read_input(
            "id направления: ",
        )
        teacher_id = read_input("id учителя: ", required=False)
        course_id = self._repo.add(
            Course(id=None, name=name, teacher_id=teacher_id, direction_id=direction_id)
        )
        print(f"Курс добавлен (id={course_id}).")
        pause()

    def _list_all(self) -> None:
        items = self._repo.get_all()
        if not items:
            print("Курсы не найдены.")
        for item in items:
            print(
                f"[{item.id}] {item.name} —  Teacher_id = {item.teacher_id}, Direction_id = {item.direction_id}"
            )
        pause()

    def _edit(self) -> None:
        course_id = read_int("ID курса: ")
        if course_id is None:
            return
        item = self._repo.get_by_id(course_id)
        if item is None:
            print("Курс не найден.")
            pause()
            return
        name = read_input(f"Название [{item.name}]: ", required=False) or item.name
        teacher_id = (
            read_input(f"teacher_id [{item.teacher_id}]: ", required=False)
            or item.teacher_id
        )
        direction_id = (
            read_input(f"direction_id [{item.direction_id}]: ", required=False)
            or item.direction_id
        )
        try:
            updated = self._repo.update(
                Course(
                    id=item.id,
                    name=name,
                    teacher_id=teacher_id,
                    direction_id=direction_id,
                )
            )
        except ValueError as exc:
            print(exc)
            pause()
            return

        if updated:
            print("Курс обновлён.")
        else:
            print("Не удалось обновить.")
        pause()

    def _delete(self) -> None:
        course_id = read_int("ID курса: ")
        if course_id is None:
            return
        if self._repo.delete(course_id):
            print("Курс удален.")
        else:
            print("Курс не найден.")
        pause()
