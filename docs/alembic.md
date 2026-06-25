# Alembic — минимальная настройка

Краткий гайд по тому, как подключить Alembic в проекте. Схема БД управляется только миграциями, без `init_schema`.

---

## 1. Зависимости

В `requirements.txt`:

```
SQLAlchemy>=2.0,<3
alembic>=1.13,<2
```

Установка:

```bash
pip install -r requirements.txt
```

---

## 2. Инициализация Alembic

Из корня проекта:

```bash
alembic init migrations
```

Появятся `alembic.ini` и папка `migrations/` с `env.py`.

В `alembic.ini` оставить пустой URL — он задаётся в `env.py`:

```ini
[alembic]
script_location = %(here)s/migrations
prepend_sys_path = .

sqlalchemy.url =
```

---

## 3. Базовый класс ORM

`models/base.py`:

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass
```

---

## 4. ORM-модель (пример: направление)

Dataclass `Direction` в `models/entities.py` остаётся для репозиториев.  
Для Alembic — отдельный класс `DirectionModel`:

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

> Одна ORM-модель = одна таблица в metadata. Импортируйте её в `env.py`, чтобы Alembic видел таблицу при autogenerate.

---

## 5. Подключение БД в `migrations/env.py`

Минимальные правки поверх шаблона Alembic:

```python
from database.connection import DEFAULT_DB_PATH
from models.base import Base
import models.direction_model  # noqa: F401 — регистрация модели в metadata

config.set_main_option(
  "sqlalchemy.url",
  f"sqlite:///{DEFAULT_DB_PATH.as_posix()}",
)

target_metadata = Base.metadata
```

`DEFAULT_DB_PATH` — путь к `data/portal.db`, тот же, что использует приложение.

---

## 6. Убрать `init_schema`

Из `web/db.py` и `cli/menu.py` убрать вызов `init_schema`.  
Таблицы создаются только через:

```bash
alembic upgrade head
```

---

## 7. Создание и применение миграции

Пустая БД:

```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

Проверка текущей версии:

```bash
alembic current
```

Новая модель (например, добавили `TeacherModel`):

1. Создать `models/teacher_model.py`
2. Добавить `import models.teacher_model  # noqa: F401` в `env.py`
3. `alembic revision --autogenerate -m "add teachers"`
4. `alembic upgrade head`

---