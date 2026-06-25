"""Репозиторий учебных направлений."""

from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from models.entities import Direction
from models.direction_model import DirectionModel
from database.session import SessionLocal
from repositories.interfaces import IDirectionRepository


class DirectionRepository(IDirectionRepository):
    """CRUD-операции для направлений."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, direction: Direction) -> int:
        """Добавить направление."""
        direction_model = DirectionModel(
            name=direction.name, description=direction.description
        )
        self._session.add(direction_model)
        self._session.commit()
        return direction_model.id

    def get_by_id(self, direction_id: int) -> Optional[Direction]:
        """Получить направление по ID."""
        direction_model = self._session.get(DirectionModel, direction_id)
        if direction_model is None:
            return None
        return self._model_to_dataclass(direction_model)

    def get_all(self) -> list[Direction]:
        """Получить все направления."""
        stmt = select(DirectionModel).order_by(DirectionModel.name)
        directions: list[DirectionModel] = self._session.scalars(stmt).all()
        return [self._model_to_dataclass(direction) for direction in directions]

    def update(self, direction: Direction) -> bool:
        """Обновить направление."""
        if direction.id is None:
            return False
        direction_model = self._session.get(DirectionModel, direction.id)
        direction_model.name = direction.name
        direction_model.description = direction.description
        self._session.commit()
        return True

    def delete(self, direction_id: int) -> bool:
        """Удалить направление."""
        direction_model = self._session.get(DirectionModel, direction_id)
        if direction_model is not None:
            self._session.delete(direction_model)
            self._session.commit()
            return True
        return False

    @staticmethod
    def _model_to_dataclass(model: DirectionModel) -> Direction:
        return Direction(
            id=model.id,
            name=model.name,
            description=model.description,
        )


if __name__ == "__main__":
    with SessionLocal() as session:
        repo = DirectionRepository(session)
        # dir1 = Direction(id=None, name="прога")
        # repo.add(dir1)
        directions = repo.get_all()
        print(directions)
