"""Консольное меню учебного портала."""

from cli.helpers import pause, read_input, read_int
from database.connection import Database
from database.schemas import init_schema
from models.entities import Direction
from repositories.directions import DirectionRepository
from repositories.teachers import TeacherRepository


class PortalApp:
    """Главное консольное приложение."""

    def __init__(self, db: Database) -> None:
        self._db = db
        self._directions_repo = DirectionRepository(db)
        self._teachers_repo = TeacherRepository(db)

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
        # print("2. Преподаватели")

    def _dispatch(self, choice: str) -> None:
        handlers = {
            "1": self._direction_menu,
            # "2": self._teacher_menu, #todo
        }
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("Неверный пункт меню.")

    # --- Направления ---

    def _direction_menu(self) -> None:
        while True:
            print("\n--- Направления ---")
            print("1. Добавить  2. Показать все  3. Редактировать")
            print("4. Удалить 0. Назад")
            choice = read_input("Выберите: ")
            if choice == "0":
                return
            if choice == "1":
                self._add_direction()
            elif choice == "2":
                self._list_directions()
            elif choice == "3":
                self._edit_direction()
            elif choice == "4":
                self._delete_direction()
            else:
                print("Неверный пункт.")

    def _add_direction(self) -> None:
        name = read_input("Название: ")
        description = read_input("Описание: ", required=False)
        direction_id = self._directions_repo.add(
            Direction(id=None, name=name, description=description)
        )
        print(f"Направление добавлено (id={direction_id}).")
        pause()

    def _list_directions(self) -> None:
        items = self._directions_repo.get_all()
        if not items:
            print("Направления не найдены.")
        for item in items:
            print(f"[{item.id}] {item.name} — {item.description or 'без описания'}")
        pause()

    def _edit_direction(self) -> None:
        direction_id = read_int("ID направления: ")
        if direction_id is None:
            return
        item = self._directions_repo.get_by_id(direction_id)
        if item is None:
            print("Направление не найдено.")
            pause()
            return
        name = read_input(f"Название [{item.name}]: ", required=False) or item.name
        description = read_input(f"Описание [{item.description}]: ", required=False)
        if description == "":
            description = item.description
        updated = Direction(id=item.id, name=name, description=description)
        if self._directions_repo.update(updated):
            print("Направление обновлено.")
        else:
            print("Не удалось обновить.")
        pause()

    def _delete_direction(self) -> None:
        direction_id = read_int("ID направления: ")
        if direction_id is None:
            return
        if self._directions_repo.delete(direction_id):
            print("Направление удалено.")
        else:
            print("Направление не найдено.")
        pause()
