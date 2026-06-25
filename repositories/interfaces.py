"""Интерфейсы (абстрактные контракты) репозиториев."""

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from models.entities import Course, Direction, Student, StudentResult, Teacher

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    """Базовый интерфейс репозитория с CRUD-операциями."""

    @abstractmethod
    def add(self, entity: T) -> int:
        """Добавить сущность и вернуть её ID."""

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Получить сущность по ID."""

    @abstractmethod
    def get_all(self) -> list[T]:
        """Получить все сущности."""

    @abstractmethod
    def update(self, entity: T) -> bool:
        """Обновить сущность."""

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Удалить сущность по ID."""


# class ISearchableRepository(IRepository[T], ABC):
#     """Интерфейс репозитория с поиском по частичному совпадению имени."""

#     @abstractmethod
#     def search_by_name(self, pattern: str) -> list[T]:
#         """Найти сущности по фрагменту имени или названия."""


class IDirectionRepository(IRepository[Direction], ABC):
    """Интерфейс репозитория учебных направлений."""

    pass
    # @abstractmethod
    # def get_by_name(self, name: str) -> Optional[Direction]:
    #     """Получить направление по точному названию."""


class ITeacherRepository(IRepository[Teacher], ABC):
    """Интерфейс репозитория учителей."""

    pass
    # @abstractmethod
    # def get_by_name(self, name: str) -> Optional[Direction]:
    #     """Получить направление по точному названию."""


class IStudentsRepository(IRepository[Student], ABC):
    """Интерфейс репозитория студентов."""

    pass


class ICourseRepository(IRepository[Course], ABC):
    """Интерфейс репозитория курсов"""

    pass


class IResultRepository(IRepository[StudentResult], ABC):
    """Интерфейс репозитория оценок студентов."""

    @abstractmethod
    def get_by_student(self, student_id: int) -> list[StudentResult]:
        """Получить оценки студента."""

    @abstractmethod
    def get_by_course(self, course_id: int) -> list[StudentResult]:
        """Получить оценки по курсу."""
