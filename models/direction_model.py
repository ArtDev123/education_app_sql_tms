from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class DirectionModel(Base):
    __tablename__ = "directions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=False, server_default="")
