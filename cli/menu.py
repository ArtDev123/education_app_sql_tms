"""Консольное меню учебного портала."""

from cli.directions import DirectionDispatcher
from cli.helpers import read_input
from database.connection import Database
from database.schemas import init_schema
from repositories.directions import DirectionRepository


class PortalApp:
    """Главное консольное приложение."""

    def __init__(self, db: Database) -> None:
        self._db = db
        self._directions = DirectionDispatcher(DirectionRepository(db))

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

    def _dispatch(self, choice: str) -> None:
        handlers = {
            "1": self._directions.run,
        }
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("Неверный пункт меню.")
