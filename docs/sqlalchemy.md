# SQLAlchemy — основы

Краткий гайд по ORM в стиле SQLAlchemy 2.0. Примеры на модели `DirectionModel` — той же, что в [гайде по Alembic](alembic.md).

В проекте сейчас репозитории работают через raw SQL (`database/connection.py`). ORM-модели нужны для Alembic и могут использоваться для CRUD напрямую.

---

## 1. Основные понятия

| Термин | Что это |
|--------|---------|
| **Engine** | Подключение к БД (драйвер + URL) |
| **Session** | «Рабочая сессия» — через неё читаем и пишем объекты |
| **Model** | Python-класс ↔ строка таблицы |
| **Base** | Общий родитель для всех моделей, хранит metadata |

Цепочка: `Engine` → `Session` → запросы к `Model`.

---

## 2. Базовый класс и модель

`models/base.py`:

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass
```

`models/direction_model.py`:

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class DirectionModel(Base):
  __tablename__ = "directions"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
  description: Mapped[str] = mapped_column(String, nullable=False, server_default="")
```

### Как читать объявление полей

```python
id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
```

- `Mapped[int]` — тип колонки в Python
- `mapped_column(...)` — настройки колонки в БД
- `primary_key=True` — первичный ключ
- `nullable=False` — поле обязательно
- `unique=True` — уникальное значение
- `server_default=""` — значение по умолчанию на стороне БД

> Имя класса (`DirectionModel`) — для кода. Имя таблицы — `__tablename__ = "directions"`.

---

## 3. Engine и Session

Файл `database/session.py` (пример для проекта):

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database.connection import DEFAULT_DB_PATH

engine = create_engine(
  f"sqlite:///{DEFAULT_DB_PATH.as_posix()}",
  echo=False,  # True — печатать SQL в консоль (удобно при отладке)
)

SessionLocal = sessionmaker(bind=engine)
```

Использование:

```python
with SessionLocal() as session:
  # работа с БД
  session.commit()  # сохранить изменения
```

Если забыть `commit()` — INSERT/UPDATE/DELETE не попадут в БД.

---

## 4. CREATE — добавить запись

```python
from models.direction_model import DirectionModel

with SessionLocal() as session:
  direction = DirectionModel(
    name="Программирование",
    description="Разработка ПО",
  )
  session.add(direction)
  session.commit()

  print(direction.id)  # id появится после commit
```

Несколько записей за раз:

```python
with SessionLocal() as session:
  session.add_all([
    DirectionModel(name="Дизайн", description="UI/UX"),
    DirectionModel(name="Аналитика", description="Данные"),
  ])
  session.commit()
```

---

## 5. READ — получить данные

### По id

```python
with SessionLocal() as session:
  direction = session.get(DirectionModel, 1)
  if direction is None:
    print("Не найдено")
  else:
    print(direction.name)
```

### Все записи

```python
from sqlalchemy import select

with SessionLocal() as session:
  stmt = select(DirectionModel).order_by(DirectionModel.name)
  directions = session.scalars(stmt).all()

  for d in directions:
    print(d.id, d.name)
```

### С фильтром

```python
with SessionLocal() as session:
  stmt = select(DirectionModel).where(DirectionModel.name == "Программирование")
  direction = session.scalars(stmt).first()  # одна запись или None
```

### Поиск по части строки

```python
with SessionLocal() as session:
  stmt = select(DirectionModel).where(DirectionModel.name.contains("Про"))
  results = session.scalars(stmt).all()
```

### Только нужные колонки

```python
with SessionLocal() as session:
  stmt = select(DirectionModel.id, DirectionModel.name)
  rows = session.execute(stmt).all()
  # [(1, 'Программирование'), (2, 'Дизайн'), ...]
```

---

## 6. UPDATE — обновить запись

```python
with SessionLocal() as session:
  direction = session.get(DirectionModel, 1)
  if direction is not None:
    direction.name = "Разработка ПО"
    direction.description = "Backend и frontend"
    session.commit()
```

SQLAlchemy отслеживает изменения объекта в сессии — отдельный `UPDATE`-запрос писать не нужно.

Массовое обновление без загрузки объектов:

```python
from sqlalchemy import update

with SessionLocal() as session:
  stmt = (
    update(DirectionModel)
    .where(DirectionModel.name == "Дизайн")
    .values(description="Графический дизайн")
  )
  session.execute(stmt)
  session.commit()
```

---

## 7. DELETE — удалить запись

### Одна запись

```python
with SessionLocal() as session:
  direction = session.get(DirectionModel, 1)
  if direction is not None:
    session.delete(direction)
    session.commit()
```

### Несколько по условию

```python
from sqlalchemy import delete

with SessionLocal() as session:
  stmt = delete(DirectionModel).where(DirectionModel.name == "Аналитика")
  session.execute(stmt)
  session.commit()
```

---

## 8. CRUD в одной шпаргалке

```python
from sqlalchemy import delete, select, update

# CREATE
session.add(DirectionModel(name="...", description="..."))

# READ
session.get(DirectionModel, id)
session.scalars(select(DirectionModel)).all()
session.scalars(select(DirectionModel).where(...)).first()

# UPDATE
obj = session.get(DirectionModel, id)
obj.name = "новое имя"

# DELETE
session.delete(obj)

session.commit()
```

---

## 9. Обработка ошибок

При нарушении уникальности (`name` уже есть) SQLite выбросит исключение:

```python
from sqlalchemy.exc import IntegrityError

with SessionLocal() as session:
  try:
    session.add(DirectionModel(name="Программирование", description=""))
    session.commit()
  except IntegrityError:
    session.rollback()
    print("Направление с таким именем уже существует")
```

`rollback()` откатывает незакоммиченные изменения в текущей сессии.

---

## 10. ORM-модель и dataclass

В проекте два слоя:

| Слой | Файл | Назначение |
|------|------|------------|
| Dataclass | `models/entities.py` → `Direction` | Репозитории, Flask, CLI |
| ORM | `models/direction_model.py` → `DirectionModel` | Alembic, SQLAlchemy CRUD |

Преобразование ORM → dataclass:

```python
from models.entities import Direction

def to_entity(model: DirectionModel) -> Direction:
  return Direction(
    id=model.id,
    name=model.name,
    description=model.description,
  )
```

---

## 11. Связь с Alembic

Модель сама по себе таблицу не создаёт. Схема управляется миграциями:

```bash
alembic revision --autogenerate -m "add directions"
alembic upgrade head
```

Подробнее — в [docs/alembic.md](alembic.md).

---

## 12. Частые ошибки

| Проблема | Причина | Решение |
|----------|---------|---------|
| Изменения не сохраняются | Нет `commit()` | Вызвать `session.commit()` |
| `no such table: directions` | Миграция не применена | `alembic upgrade head` |
| Объект «отсоединился» от сессии | Сессия закрыта, объект снова читают | Читать поля внутри `with SessionLocal()` или передать в dataclass |
| Дублирование `name` | `unique=True` на колонке | Проверять перед вставкой или ловить `IntegrityError` |
