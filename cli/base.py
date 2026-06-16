"""Базовый класс диспетчеров консольного меню."""

from abc import ABC, abstractmethod

from cli.helpers import read_input


class CrudDispatcher(ABC):
    """Базовый диспетчер CRUD-меню."""

    @property
    @abstractmethod
    def _title(self) -> str:
        """Заголовок подменю."""

    @abstractmethod
    def _add(self) -> None:
        """Добавить сущность."""

    @abstractmethod
    def _list_all(self) -> None:
        """Показать все сущности."""

    @abstractmethod
    def _edit(self) -> None:
        """Редактировать сущность."""

    @abstractmethod
    def _delete(self) -> None:
        """Удалить сущность."""

    def run(self) -> None:
        while True:
            print(f"\n--- {self._title} ---")
            print("1. Добавить  2. Показать все  3. Редактировать")
            print("4. Удалить 0. Назад")
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
            else:
                print("Неверный пункт.")
