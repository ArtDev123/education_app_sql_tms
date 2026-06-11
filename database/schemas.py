from database.connection import Database

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS directions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT    NOT NULL DEFAULT ''
);
"""

def init_schema(db: Database) -> None:
    """Создать таблицы, если они ещё не существуют."""
    db.connect().executescript(SCHEMA_SQL)
    db.connect().commit()

if __name__ == "__main__":
    with Database() as db:
        init_schema(db)