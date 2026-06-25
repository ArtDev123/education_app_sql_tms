from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database.connection import DEFAULT_DB_PATH

engine = create_engine(
    f"sqlite:///{DEFAULT_DB_PATH.as_posix()}",
    echo=True,  # True — печатать SQL в консоль (удобно при отладке)
)

SessionLocal = sessionmaker(bind=engine)
