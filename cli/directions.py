"""Диспетчер меню направлений."""

from cli.base import CrudDispatcher
from cli.helpers import pause, read_input, read_int
from models.entities import Direction
from repositories.directions import DirectionRepository


class DirectionDispatcher(CrudDispatcher):
    """Консольное меню направлений."""

    def __init__(self, repo: DirectionRepository) -> None:
        self._repo = repo

    @property
    def _title(self) -> str:
        return "Направления"

    def _add(self) -> None:
        name = read_input("Название: ")
        description = read_input("Описание: ", required=False)
        direction_id = self._repo.add(
            Direction(id=None, name=name, description=description)
        )
        print(f"Направление добавлено (id={direction_id}).")
        pause()

    def _list_all(self) -> None:
        items = self._repo.get_all()
        if not items:
            print("Направления не найдены.")
        for item in items:
            print(f"[{item.id}] {item.name} — {item.description or 'без описания'}")
        pause()

    def _edit(self) -> None:
        direction_id = read_int("ID направления: ")
        if direction_id is None:
            return
        item = self._repo.get_by_id(direction_id)
        if item is None:
            print("Направление не найдено.")
            pause()
            return
        name = read_input(f"Название [{item.name}]: ", required=False) or item.name
        description = read_input(f"Описание [{item.description}]: ", required=False)
        if description == "":
            description = item.description
        updated = Direction(id=item.id, name=name, description=description)
        if self._repo.update(updated):
            print("Направление обновлено.")
        else:
            print("Не удалось обновить.")
        pause()

    def _delete(self) -> None:
        direction_id = read_int("ID направления: ")
        if direction_id is None:
            return
        if self._repo.delete(direction_id):
            print("Направление удалено.")
        else:
            print("Направление не найдено.")
        pause()
