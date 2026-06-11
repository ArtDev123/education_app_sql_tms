# Техническое задание

## Консольное приложение «Учебный портал»

**Вариант:** 3 — Учебный портал  
**Тип:** консольное приложение  
**СУБД:** SQLite  
**Доступ к данным:** raw SQL (без ORM)  
**Язык:** Python 3.10+

---

## 1. Цель проекта

Разработать консольное приложение для управления учебным порталом. Система должна хранить данные о направлениях обучения, курсах, преподавателях, студентах и их оценках, предоставлять базовые CRUD-операции, поиск и аналитику успеваемости.

Приложение предназначено для демонстрации работы с реляционной базой данных через прямые SQL-запросы.

---

## 2. Технологический стек

| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.10+ |
| БД | SQLite (`sqlite3` из стандартной библиотеки) |
| Виртуальное окружение | `venv` |
| Типизация | `typing`, `dataclasses`, проверка через `mypy` |
| Стиль кода | PEP 8, проверка через `flake8` |
| Сборка / проверки | `Makefile` |
| Зависимости runtime | не требуются (только stdlib) |
| Зависимости dev | `flake8`, `mypy` (`requirements-dev.txt`) |

---

## 3. Структура проекта

```
education_system/
├── main.py                  # Точка входа
├── Makefile                 # Команды запуска и проверки кода
├── setup.cfg                # Настройки flake8 и mypy
├── requirements.txt         # Runtime-зависимости (пустой — только stdlib)
├── requirements-dev.txt     # Dev-зависимости (flake8, mypy)
├── data/
│   └── portal.db            # Файл БД (создаётся автоматически)
├── models/
│   ├── __init__.py
│   └── entities.py          # Dataclass-модели сущностей
├── database/
│   ├── __init__.py
│   ├── connection.py        # Подключение к SQLite
│   └── schema.py            # DDL-схема (CREATE TABLE)
├── repositories/
│   ├── __init__.py
│   ├── interfaces.py        # Абстрактные интерфейсы репозиториев
│   ├── base.py              # Общие утилиты
│   ├── directions.py        # CRUD направлений
│   ├── teachers.py          # CRUD преподавателей
│   ├── courses.py           # CRUD курсов
│   ├── students.py          # CRUD студентов
│   └── results.py           # CRUD оценок
├── services/
│   ├── __init__.py
│   └── analytics.py         # Аналитика успеваемости
└── cli/
    ├── __init__.py
    ├── helpers.py           # Ввод данных из консоли
    └── menu.py              # Меню и обработчики команд
```

---

## 4. Модели данных

Все модели реализуются как `@dataclass` в `models/entities.py`.

### 4.1. Direction — учебное направление

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `Optional[int]` | Первичный ключ |
| `name` | `str` | Название (уникальное) |
| `description` | `str` | Описание |

### 4.2. Teacher — преподаватель

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `Optional[int]` | Первичный ключ |
| `first_name` | `str` | Имя |
| `last_name` | `str` | Фамилия |
| `email` | `str` | Email |
| `phone` | `str` | Телефон |

### 4.3. Course — курс

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `Optional[int]` | Первичный ключ |
| `name` | `str` | Название |
| `direction_id` | `int` | FK → `directions.id` |
| `description` | `str` | Описание |
| `teacher_id` | `Optional[int]` | FK → `teachers.id` |

### 4.4. Student — студент

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `Optional[int]` | Первичный ключ |
| `first_name` | `str` | Имя |
| `last_name` | `str` | Фамилия |
| `direction_id` | `int` | FK → `directions.id` |
| `email` | `str` | Email |
| `enrollment_date` | `Optional[date]` | Дата зачисления |

### 4.5. StudentResult — оценка студента

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `Optional[int]` | Первичный ключ |
| `student_id` | `int` | FK → `students.id` |
| `course_id` | `int` | FK → `courses.id` |
| `grade` | `float` | Оценка (1.0–5.0) |
| `exam_date` | `Optional[date]` | Дата экзамена |

---

## 5. Интерфейсы репозиториев

Перед реализацией конкретных классов описать абстрактные контракты в `repositories/interfaces.py` с помощью `abc.ABC` и `typing.Generic`.

### 5.1. Иерархия интерфейсов

```
IRepository[T]                    ← базовый CRUD
    │
    ├── ISearchableRepository[T]  ← + search_by_name()
    │       ├── IDirectionRepository
    │       ├── ITeacherRepository
    │       ├── ICourseRepository
    │       └── IStudentRepository
    │
    └── IResultRepository         ← без search_by_name
```

### 5.2. IRepository[T] — базовый интерфейс

Общий контракт для всех репозиториев:

| Метод | Сигнатура | Описание |
|-------|-----------|----------|
| `add` | `(entity: T) -> int` | Создать запись, вернуть ID |
| `get_by_id` | `(entity_id: int) -> Optional[T]` | Найти по ID |
| `get_all` | `() -> list[T]` | Получить все записи |
| `update` | `(entity: T) -> bool` | Обновить запись |
| `delete` | `(entity_id: int) -> bool` | Удалить по ID |

### 5.3. ISearchableRepository[T]

Расширяет `IRepository[T]`, добавляет:

| Метод | Сигнатура | Описание |
|-------|-----------|----------|
| `search_by_name` | `(pattern: str) -> list[T]` | Поиск по частичному совпадению |

### 5.4. Специализированные интерфейсы

**IDirectionRepository** (`ISearchableRepository[Direction]`):

| Метод | Сигнатура |
|-------|-----------|
| `get_by_name` | `(name: str) -> Optional[Direction]` |

**ITeacherRepository** (`ISearchableRepository[Teacher]`):

| Метод | Сигнатура |
|-------|-----------|
| `get_by_name` | `(first_name: str, last_name: str) -> Optional[Teacher]` |

**ICourseRepository** (`ISearchableRepository[Course]`):

| Метод | Сигнатура |
|-------|-----------|
| `get_by_name` | `(name: str) -> Optional[Course]` |
| `get_by_direction` | `(direction_id: int) -> list[Course]` |
| `search_by_direction_name` | `(direction_pattern: str) -> list[Course]` |

**IStudentRepository** (`ISearchableRepository[Student]`):

| Метод | Сигнатура |
|-------|-----------|
| `get_by_name` | `(first_name: str, last_name: str) -> Optional[Student]` |
| `get_by_direction` | `(direction_id: int) -> list[Student]` |

**IResultRepository** (`IRepository[StudentResult]`):

| Метод | Сигнатура |
|-------|-----------|
| `get_by_student` | `(student_id: int) -> list[StudentResult]` |
| `get_by_course` | `(course_id: int) -> list[StudentResult]` |

### 5.5. Реализация интерфейсов

Каждый конкретный репозиторий **наследует** соответствующий интерфейс:

```python
class DirectionRepository(IDirectionRepository):
    def add(self, direction: Direction) -> int:
        ...
```

**Правила:**
- интерфейс описывает *что* делает репозиторий, реализация — *как* (raw SQL);
- `cli/` и `services/` зависят от интерфейсов, а не от конкретных классов (типизация аргументов);
- все методы интерфейса помечаются `@abstractmethod`;
- нельзя создать экземпляр абстрактного класса без реализации всех методов.

### 5.6. Пример каркаса interfaces.py

```python
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")

class IRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> int: ...

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]: ...

    @abstractmethod
    def get_all(self) -> list[T]: ...

    @abstractmethod
    def update(self, entity: T) -> bool: ...

    @abstractmethod
    def delete(self, entity_id: int) -> bool: ...
```

---

## 6. Схема базы данных

Схема создаётся в `database/schema.py` через `executescript()` при первом запуске.

### 6.1. Таблицы и связи

```
directions (1) ──< courses
directions (1) ──< students
teachers   (1) ──< courses (опционально)
students   (1) ──< student_results >── courses (1)
```

### 6.2. Ограничения

- `directions.name` — `UNIQUE`
- `student_results.grade` — `CHECK (grade >= 1 AND grade <= 5)`
- `student_results (student_id, course_id)` — `UNIQUE` (одна оценка на пару студент+курс)
- Внешние ключи с `ON DELETE CASCADE` / `ON DELETE SET NULL`
- `PRAGMA foreign_keys = ON` при подключении

### 6.3. Индексы

- `courses.direction_id`
- `students.direction_id`
- `student_results.student_id`
- `student_results.course_id`

---

## 7. Функциональные требования

### 7.1. Простые операции (CRUD)

Для каждой сущности (направления, преподаватели, курсы, студенты, оценки):

| Операция | Описание |
|----------|----------|
| **Create** | Добавление новой записи |
| **Read** | Просмотр всех записей |
| **Read by name** | Поиск по точному имени/названию |
| **Update** | Редактирование по ID |
| **Delete** | Удаление по ID |

Дополнительно для оценок:
- просмотр оценок по студенту;
- просмотр оценок по курсу.

### 7.2. Сложные операции (поиск)

| Операция | Реализация |
|----------|------------|
| Поиск курса по части названия | `CourseRepository.search_by_name()` |
| Поиск курса по направлению | `CourseRepository.search_by_direction_name()` (JOIN) |
| Поиск преподавателя по части имени | `TeacherRepository.search_by_name()` |
| Поиск студента по части имени | `StudentRepository.search_by_name()` |
| Поиск направления по части названия | `DirectionRepository.search_by_name()` |

Поиск должен быть регистронезависимым, в том числе для кириллицы (через `str.casefold()` в Python, а не через `LOWER()` SQLite).

### 7.3. Аналитика прогресса

Сервис `AnalyticsService` в `services/analytics.py`. Порог сдачи: **3.0**.

| Метод | Описание |
|-------|----------|
| `get_student_progress(student_id)` | Прогресс одного студента |
| `get_all_students_progress()` | Прогресс всех студентов |
| `get_direction_progress(direction_id)` | Прогресс студентов направления |
| `get_course_statistics(course_id)` | Статистика по курсу |
| `get_underperforming_students(threshold)` | Студенты со средним баллом ниже порога |

**Показатели прогресса студента:**
- средний балл (`AVG`);
- количество оценок;
- минимальная / максимальная оценка;
- количество сданных курсов (оценка ≥ 3);
- количество несданных курсов (оценка < 3).

**Показатели по курсу:**
- количество студентов с оценками;
- средний балл;
- процент сдавших.

---

## 8. Консольный интерфейс

### 8.1. Главное меню

```
--- Главное меню ---
1. Направления
2. Преподаватели
3. Курсы
4. Студенты
5. Оценки
6. Поиск
7. Аналитика прогресса
0. Выход
```

### 8.2. Подменю сущностей (пример — направления)

```
--- Направления ---
1. Добавить
2. Показать все
3. Найти по названию
4. Редактировать
5. Удалить
0. Назад
```

Аналогичная структура для преподавателей, курсов, студентов. Для оценок — пункты «по студенту» и «по курсу» вместо поиска по имени.

### 8.3. Меню поиска

```
--- Поиск ---
1. Курсы по части названия
2. Курсы по направлению (частичное совпадение)
3. Преподаватели по части имени
4. Студенты по части имени
5. Направления по части названия
0. Назад
```

### 8.4. Меню аналитики

```
--- Аналитика прогресса ---
1. Прогресс студента (по ID)
2. Прогресс всех студентов
3. Прогресс по направлению (по ID)
4. Статистика по курсу (по ID)
5. Студенты с низкой успеваемостью
0. Назад
```

### 8.5. Требования к вводу

Реализовать в `cli/helpers.py`:

- `read_input()` — строка с проверкой обязательности;
- `read_int()` — целое число;
- `read_float()` — число с плавающей точкой;
- `read_date()` — дата в формате `ГГГГ-ММ-ДД`;
- `pause()` — ожидание Enter перед возвратом в меню.

При неверном вводе — повторный запрос, без падения приложения.

---

## 9. Архитектура и слои

```
┌─────────────────────────────────────┐
│           cli/menu.py               │  ← пользовательский интерфейс
├─────────────────────────────────────┤
│  repositories/*.py   services/      │  ← реализация доступа к данным
│  repositories/interfaces.py         │  ← абстрактные контракты
├─────────────────────────────────────┤
│  database/connection.py + schema.py │  ← raw SQL, SQLite
├─────────────────────────────────────┤
│  models/entities.py                 │  ← структуры данных
└─────────────────────────────────────┘
```

**Правила:**
- SQL-запросы пишутся только в `repositories/` и `services/`;
- `cli/` не содержит SQL, только вызывает репозитории и сервисы;
- каждый репозиторий реализует соответствующий интерфейс из `interfaces.py`;
- каждый репозиторий принимает `Database` в конструкторе;
- параметризованные запросы (`?`) — защита от SQL-инъекций.

---

## 10. Порядок реализации

### Этап 1. Окружение и каркас

1. Создать виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Создать структуру каталогов (см. раздел 3).
3. Добавить `requirements.txt`, `requirements-dev.txt`, `setup.cfg`, `Makefile`
   и `.gitignore` (`venv/`, `data/`, `__pycache__/`).

### Этап 2. Модели

1. Описать все dataclass в `models/entities.py`.
2. Экспортировать модели из `models/__init__.py`.

### Этап 3. База данных

1. Реализовать класс `Database` в `database/connection.py`:
   - подключение к `data/portal.db`;
   - `row_factory = sqlite3.Row`;
   - методы `execute()`, `fetchone()`, `fetchall()`;
   - контекстный менеджер (`with Database() as db`).
2. Написать DDL в `database/schema.py`.
3. Реализовать `init_schema(db)` — вызов при старте приложения.

### Этап 4. Интерфейсы и репозитории

1. Описать абстрактные интерфейсы в `repositories/interfaces.py`:
   - `IRepository[T]` — базовый CRUD;
   - `ISearchableRepository[T]` — с поиском;
   - `IDirectionRepository`, `ITeacherRepository`, `ICourseRepository`,
     `IStudentRepository`, `IResultRepository` — специализированные контракты.
2. Экспортировать интерфейсы из `repositories/__init__.py`.

Для каждой сущности создать класс-репозиторий, **наследующий интерфейс**, с методами:

| Метод | SQL-операция |
|-------|--------------|
| `add(entity)` | `INSERT` |
| `get_by_id(id)` | `SELECT ... WHERE id = ?` |
| `get_by_name(...)` | `SELECT ... WHERE name/first_name/last_name = ?` |
| `get_all()` | `SELECT ... ORDER BY ...` |
| `update(entity)` | `UPDATE ... WHERE id = ?` |
| `delete(id)` | `DELETE ... WHERE id = ?` |
| `search_by_name(pattern)` | выборка + фильтр `casefold()` в Python |

Для курсов дополнительно:
- `get_by_direction(direction_id)`;
- `search_by_direction_name(pattern)` — `JOIN directions`.

В `repositories/base.py`:
- `parse_date()` / `format_date()` — конвертация дат;
- `matches_partial()` — регистронезависимый поиск.

### Этап 5. Аналитика

1. Описать dataclass `StudentProgress` и `CourseStatistics`.
2. Реализовать `AnalyticsService` с агрегирующими SQL-запросами:
   - `JOIN` студентов с направлениями и оценками;
   - `AVG`, `MIN`, `MAX`, `COUNT`;
   - `CASE WHEN` для подсчёта сданных/несданных;
   - `HAVING` для фильтрации по среднему баллу.

### Этап 6. Консольный интерфейс

1. Реализовать `cli/helpers.py` — функции ввода.
2. Реализовать `cli/menu.py` — класс `PortalApp`:
   - инициализация репозиториев и сервиса аналитики;
   - главный цикл с меню;
   - обработчики для каждого пункта;
   - валидация (существование FK, диапазон оценок 1–5).
3. Реализовать `main.py`:
   ```python
   with Database() as db:
       PortalApp(db).run()
   ```

### Этап 7. Makefile и линтеры

1. Создать `requirements-dev.txt` (`flake8`, `mypy`).
2. Настроить `setup.cfg` для обоих инструментов.
3. Добавить `Makefile` с целями `flake8`, `mypy`, `lint`.
4. Исправить замечания до успешного `make lint`.

### Этап 8. Проверка

Прогнать сценарии из раздела 11 и выполнить `make lint`.

---

## 11. Сценарии приёмки

### 11.1. Базовый сценарий

1. Добавить направление «Информатика».
2. Добавить преподавателя «Петров Иван».
3. Добавить курс «Базы данных» (направление: Информатика, преподаватель: Петров).
4. Добавить студента «Иванов Алексей» (направление: Информатика).
5. Выставить оценку 4.5 по курсу «Базы данных».
6. Найти курс по фрагменту «баз» — должен найтись.
7. Посмотреть прогресс студента — средний балл 4.5.

### 11.2. Каскадное удаление

1. Удалить направление.
2. Убедиться, что связанные курсы и студенты тоже удалены.

### 11.3. Уникальность оценки

1. Попытаться добавить вторую оценку тому же студенту по тому же курсу.
2. Приложение должно вывести ошибку, а не упасть.

### 11.4. Аналитика

1. Создать двух студентов с разной успеваемостью.
2. Запросить «студентов с низкой успеваемостью» (порог 3.0).
3. В списке — только студенты со средним баллом < 3.0.

---

## 12. Нефункциональные требования

| Требование | Как выполнить |
|------------|---------------|
| Типизация | Аннотации типов для всех функций и методов |
| PEP 8 | Имена в `snake_case`, отступы 4 пробела, docstring у модулей и классов |
| venv | Разработка и запуск только внутри виртуального окружения |
| Raw SQL | Запрещены ORM (SQLAlchemy, Peewee и т.п.) |
| Обработка ошибок | Валидация ввода в CLI, перехват `sqlite3.IntegrityError` |
| Документация | Docstring на русском языке у публичных методов |
| Статический анализ | `make lint` проходит без ошибок |

---

## 13. Makefile и проверка качества кода

### 13.1. Файлы

| Файл | Назначение |
|------|------------|
| `Makefile` | Команды для установки, запуска и проверки |
| `setup.cfg` | Конфигурация `flake8` и `mypy` |
| `requirements-dev.txt` | Dev-зависимости: `flake8`, `mypy` |

### 13.2. Команды Makefile

| Команда | Описание |
|---------|----------|
| `make install` | Создать `venv` и установить `requirements.txt` |
| `make install-dev` | Установить dev-зависимости |
| `make flake8` | Проверка стиля кода (PEP 8) |
| `make mypy` | Проверка аннотаций типов |
| `make lint` | Запустить `flake8` и `mypy` |
| `make run-cli` | Запустить консольное приложение |
| `make clean` | Удалить `__pycache__` |

### 13.3. Настройки flake8 (`setup.cfg`)

```ini
[flake8]
max-line-length = 110
exclude = venv, .venv, __pycache__, data
```

Проверяются каталоги: `cli`, `database`, `models`, `repositories`, `services`, `main.py`.

### 13.4. Настройки mypy (`setup.cfg`)

```ini
[mypy]
python_version = 3.10
check_untyped_defs = True
ignore_missing_imports = True
```

`mypy` проверяет те же исходники, что и `flake8`.

### 13.5. Порядок внедрения

1. Создать `requirements-dev.txt` с `flake8` и `mypy`.
2. Добавить `setup.cfg` с настройками линтеров.
3. Создать `Makefile` с целями `flake8`, `mypy`, `lint`.
4. Исправить замечания до прохождения `make lint`.
5. Запускать `make lint` перед сдачей проекта.

---

## 14. Запуск

```bash
cd education_system
make install-dev
make run-cli
```

Или вручную:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
python main.py --cli
```

База данных создаётся автоматически в `data/portal.db` при первом запуске.

Проверка кода:

```bash
make lint
```

---

## 15. Критерии готовности

- [ ] Описаны и реализованы интерфейсы репозиториев (`interfaces.py`)
- [ ] Каждый репозиторий наследует соответствующий интерфейс
- [ ] Все 5 сущностей имеют полный CRUD через консоль
- [ ] Поиск по частичному совпадению работает для всех сущностей
- [ ] Поиск курсов по направлению реализован через JOIN
- [ ] Аналитика выводит средний балл, сдано/не сдано
- [ ] Все SQL-запросы параметризованы
- [ ] Код типизирован и соответствует PEP 8
- [ ] `make lint` проходит без ошибок (`flake8` + `mypy`)
- [ ] Приложение запускается через `venv` без runtime-зависимостей
- [ ] Данные сохраняются между запусками
