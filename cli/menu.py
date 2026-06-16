"""Консольное меню учебного портала."""

from cli.directions import DirectionDispatcher
from cli.helpers import read_input
from cli.students import StudentDispatcher
from cli.teachers import TeacherDispatcher
from database.connection import Database
from database.schemas import init_schema
from repositories.directions import DirectionRepository
from repositories.students import StudentRepository
from repositories.teachers import TeacherRepository


class PortalApp:
    """Главное консольное приложение."""

    def __init__(self, db: Database) -> None:
        self._db = db
        self._directions = DirectionDispatcher(DirectionRepository(db))
        self._teachers = TeacherDispatcher(TeacherRepository(db))
        self._students = StudentDispatcher(StudentRepository(db))

    def run(self) -> None:
        """Запустить главный цикл приложения."""
        init_schema(self._db)
        print("=== Учебный портал ===")
        while True:
            self._print_main_menu()
            choice = read_input("Выберите пункт: ")
            if choice == "0":
                print("До свидания!")
                break
            self._dispatch(choice)

    def _print_main_menu(self) -> None:
        print("\n--- Главное меню ---")
        print("1. Направления")
        print("2. Преподаватели")
        print("3. Студенты")

    def _dispatch(self, choice: str) -> None:
        handlers = {
            "1": self._directions.run,
            "2": self._teachers.run,
            "3": self._students.run,
        }
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("Неверный пункт меню.")
