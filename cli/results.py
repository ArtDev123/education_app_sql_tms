"""Диспетчер меню оценок."""

from cli.base import CrudDispatcher
from cli.helpers import pause, read_date, read_float, read_input, read_int
from models.entities import StudentResult
from repositories.results import ResultRepository


class ResultDispatcher(CrudDispatcher):
    """Консольное меню оценок студентов."""

    def __init__(self, repo: ResultRepository) -> None:
        self._repo = repo

    @property
    def _title(self) -> str:
        return "Оценки"

    def run(self) -> None:
        while True:
            print(f"\n--- {self._title} ---")
            print("1. Добавить  2. Показать все  3. Редактировать")
            print("4. Удалить  5. По студенту  6. По курсу  0. Назад")
            choice = read_input("Выберите: ")
            if choice == "0":
                return
            if choice == "1":
                self._add()
            elif choice == "2":
                self._list_all()
            elif choice == "3":
                self._edit()
            elif choice == "4":
                self._delete()
            elif choice == "5":
                self._list_by_student()
            elif choice == "6":
                self._list_by_course()
            else:
                print("Неверный пункт.")

    def _add(self) -> None:
        student_id = read_int("ID студента: ")
        if student_id is None:
            return
        course_id = read_int("ID курса: ")
        if course_id is None:
            return
        grade = read_float("Оценка (1-5): ")
        exam_date = read_date("Дата экзамена")
        try:
            result_id = self._repo.add(
                StudentResult(
                    id=None,
                    student_id=student_id,
                    course_id=course_id,
                    grade=grade,
                    exam_date=exam_date,
                )
            )
        except ValueError as exc:
            print(exc)
            pause()
            return
        print(f"Оценка добавлена (id={result_id}).")
        pause()

    def _list_all(self) -> None:
        self._print_results(self._repo.get_all(), "Оценки не найдены.")
        pause()

    def _list_by_student(self) -> None:
        student_id = read_int("ID студента: ")
        if student_id is None:
            return
        self._print_results(
            self._repo.get_by_student(student_id),
            "Оценки не найдены.",
        )
        pause()

    def _list_by_course(self) -> None:
        course_id = read_int("ID курса: ")
        if course_id is None:
            return
        self._print_results(
            self._repo.get_by_course(course_id),
            "Оценки не найдены.",
        )
        pause()

    def _edit(self) -> None:
        result_id = read_int("ID оценки: ")
        if result_id is None:
            return
        item = self._repo.get_by_id(result_id)
        if item is None:
            print("Оценка не найдена.")
            pause()
            return
        student_id = (
            read_int(f"ID студента [{item.student_id}]: ", required=False)
            or item.student_id
        )
        course_id = (
            read_int(f"ID курса [{item.course_id}]: ", required=False)
            or item.course_id
        )
        grade_input = read_input(f"Оценка [{item.grade}]: ", required=False)
        grade = float(grade_input.replace(",", ".")) if grade_input else item.grade
        exam_date = read_date("Дата экзамена") or item.exam_date
        try:
            updated = self._repo.update(
                StudentResult(
                    id=result_id,
                    student_id=student_id,
                    course_id=course_id,
                    grade=grade,
                    exam_date=exam_date,
                )
            )
        except ValueError as exc:
            print(exc)
            pause()
            return
        if updated:
            print("Оценка обновлена.")
        else:
            print("Не удалось обновить.")
        pause()

    def _delete(self) -> None:
        result_id = read_int("ID оценки: ")
        if result_id is None:
            return
        if self._repo.delete(result_id):
            print("Оценка удалена.")
        else:
            print("Оценка не найдена.")
        pause()

    @staticmethod
    def _print_results(items: list[StudentResult], empty_message: str) -> None:
        if not items:
            print(empty_message)
            return
        for item in items:
            exam = item.exam_date.isoformat() if item.exam_date else ""
            print(
                f"[{item.id}] студент={item.student_id}, курс={item.course_id}, "
                f"оценка={item.grade}, экзамен={exam or 'не указана'}"
            )
