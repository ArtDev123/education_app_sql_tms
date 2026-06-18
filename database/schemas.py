from database.connection import Database

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS directions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT    NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS teachers ( 
    id	INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name	TEXT 	NOT NULL,
    last_name	TEXT	NOT NULL,
    email	    TEXT	NOT NULL,
    phone   	TEXT	NOT NULL
);

CREATE TABLE IF NOT EXISTS courses (
    id	INTEGER PRIMARY KEY AUTOINCREMENT,
    name	TEXT	NOT NULL,
    direction_id    INTEGER NOT NULL,
    teacher_id      INTEGER,
    FOREIGN KEY (direction_id) REFERENCES directions (id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id)   REFERENCES teachers (id)   ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS students (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name      TEXT    NOT NULL,
    last_name       TEXT    NOT NULL,
    direction_id    INTEGER NOT NULL,
    email           TEXT    NOT NULL DEFAULT '',
    enrollment_date TEXT,
    FOREIGN KEY (direction_id) REFERENCES directions (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS student_results (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id  INTEGER NOT NULL,
    grade      REAL    NOT NULL CHECK (grade >= 1 AND grade <= 5),
    exam_date  TEXT,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
    FOREIGN KEY (course_id)  REFERENCES courses (id)  ON DELETE CASCADE,
    UNIQUE (student_id, course_id)
);
"""


def init_schema(db: Database) -> None:
    """Создать таблицы, если они ещё не существуют."""
    db.connect().executescript(SCHEMA_SQL)
    db.connect().commit()


if __name__ == "__main__":
    print("started")
    with Database() as db:
        init_schema(db)
    print("end")
