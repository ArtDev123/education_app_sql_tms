"""Консольное меню учебного портала."""

from cli.helpers import pause, read_input, read_int, read_date
from database.connection import Database
from database.schemas import init_schema
from models.entities import Direction, Teacher, Student
from repositories.directions import DirectionRepository
from repositories.teachers import TeacherRepository
from repositories.students import StudentRepository


class PortalApp:
    """Главное консольное приложение."""

    def __init__(self, db: Database) -> None:
        self._db = db
        self._directions_repo = DirectionRepository(db)
        self._teachers_repo = TeacherRepository(db)
        self._students_repo = StudentRepository(db)

    def run(self) -> None:
        """Запустить главный цикл приложения."""
        init_schema(self._db)
        print("=== Учебный портал ===")
        while True:
            self._print_main_menu()
            choice = read_input("Выберите пункт: ")
            if choice == "0":
                print("До свидания!")
                break
            self._dispatch(choice)

    def _print_main_menu(self) -> None:
        print("\n--- Главное меню ---")
        print("1. Направления")
        print("2. Преподаватели")
        print("3. Студенты")

    def _dispatch(self, choice: str) -> None:
        handlers = {
            "1": self._direction_menu,
            "2": self._teacher_menu,
            "3": self._students_menu 
        }
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("Неверный пункт меню.")

    # --- Направления ---

    def _direction_menu(self) -> None:
        while True:
            print("\n--- Направления ---")
            print("1. Добавить  2. Показать все  3. Редактировать")
            print("4. Удалить 0. Назад")
            choice = read_input("Выберите: ")
            if choice == "0":
                return
            if choice == "1":
                self._add_direction()
            elif choice == "2":
                self._list_directions()
            elif choice == "3":
                self._edit_direction()
            elif choice == "4":
                self._delete_direction()
            else:
                print("Неверный пункт.")

    def _teacher_menu(self) -> None:
        while True:
            print("\n--- Учителя ---")
            print("1. Добавить  2. Показать все  3. Редактировать")
            print("4. Удалить 0. Назад")
            choice = read_input("Выберите: ")
            if choice == "0":
                return
            if choice == "1":
                self._add_teacher()
            elif choice == "2":
                self._list_teachers()
            elif choice == "3":
                self._edit_teacher()
            elif choice == "4":
                self._delete_teacher()
            else:
                print("Неверный пункт.")


    def _students_menu(self) -> None:
        while True:
            print("\n--- Студенты ---")
            print("1. Добавить  2. Показать все  3. Редактировать")
            print("4. Удалить 0. Назад")
            choice = read_input("Выберите: ")
            if choice == "0":
                return
            if choice == "1":
                self._add_student()
            elif choice == "2":
                self._list_students()
            elif choice == "3":
                self._edit_student()
            elif choice == "4":
                self._delete_student()
            else:
                print("Неверный пункт.")


    def _add_direction(self) -> None:
        name = read_input("Название: ")
        description = read_input("Описание: ", required=False)
        direction_id = self._directions_repo.add(
            Direction(id=None, name=name, description=description)
        )
        print(f"Направление добавлено (id={direction_id}).")
        pause()

    def _add_teacher(self) -> None:
        first_name = read_input("Имя: ")
        last_name = read_input("Фамилия: ")
        email = read_input("Email: ", required=False)
        phone = read_input("Phone: ", required=False)
        teachers_id = self._teachers_repo.add(
            Teacher(id=None, first_name=first_name, last_name=last_name, email=email, phone=phone)
        )
        print(f"Учитель добавлен (id={teachers_id}).")
        pause()

    def _add_student(self) -> None:
        first_name = read_input("Имя: ")
        last_name = read_input("Фамилия: ")
        direction_id = read_int("ID направления: ")
        if direction_id is None:
            return
        email = read_input("Email: ", required=False)
        enrollment_date = read_date("Дата зачисления")
        try:
            student_id = self._students_repo.add(
                Student(
                    id=None,
                    first_name=first_name,
                    last_name=last_name,
                    direction_id=direction_id,
                    email=email,
                    enrollment_date=enrollment_date,
                )
            )
        except ValueError as e:
            print(e)
            pause()
            return
        print(f"Студент добавлен (id={student_id}).")
        pause()

    def _list_directions(self) -> None:
        items = self._directions_repo.get_all()
        if not items:
            print("Направления не найдены.")
        for item in items:
            print(f"[{item.id}] {item.name} — {item.description or 'без описания'}")
        pause()

    def _list_teachers(self) -> None:
        items = self._teachers_repo.get_all()
        if not items:
            print("Учителя не найдены.")
        for item in items:
            print(f"[{item.id}], {item.first_name}, {item.last_name}, {item.email}, {item.phone}")
        pause()


    def _list_students(self) -> None:
        items = self._students_repo.get_all()
        if not items:
            print("Студент не найден")
        for item in items:
            print(f"[{item.id}], {item.first_name}, {item.last_name}, {item.direction_id}, {item.email}, {item.enrollment_date}")

    def _edit_direction(self) -> None:
        direction_id = read_int("ID направления: ")
        if direction_id is None:
            return
        item = self._directions_repo.get_by_id(direction_id)
        if item is None:
            print("Направление не найдено.")
            pause()
            return
        name = read_input(f"Название [{item.name}]: ", required=False) or item.name
        description = read_input(f"Описание [{item.description}]: ", required=False)
        if description == "":
            description = item.description
        updated = Direction(id=item.id, name=name, description=description)
        if self._directions_repo.update(updated):
            print("Направление обновлено.")
        else:
            print("Не удалось обновить.")
        pause()

    def _edit_teacher(self) -> None:
        teacher_id = read_int("ID учителя: ")
        if teacher_id is None:
            return
        item = self._teachers_repo.get_by_id(teacher_id)
        if item is None:
            print("Учитель не найден.")
            pause()
            return
        first_name = read_input(f"Имя [{item.first_name}]: ", required=False) or item.first_name
        last_name = read_input(f"Фамилия [{item.last_name}]: ", required=False) or item.last_name
        email = read_input(f"Email [{item.email}]: ", required=False) or item.email
        phone = read_input(f"Телефон [{item.phone}]: ", required=False) or item.phone
    
        if self._teachers_repo.update(teacher=Teacher(id=teacher_id, first_name=first_name, last_name=last_name, email=email, phone=phone)):
            print("Учитель обновлен.")
        else:
            print("Учитель не найден.")
        pause()


    def _edit_student(self) -> None:
        student_id = read_int("ID студента: ")
        if student_id is None:
            return
        
        item = self._students_repo.get_by_id(student_id)

        if item is None:
            print("Студент не найден.")
            pause()
            return
        
        first_name = (
            read_input(f"Имя [{item.first_name}]: ", required=False) or item.first_name
        )
        last_name = (
            read_input(f"Фамилия [{item.last_name}]: ", required=False)
            or item.last_name
        )
        direction_id = (
            read_int(f"ID направления [{item.direction_id}]: ", required=False)
            or item.direction_id
        )
        email = read_input(f"Email [{item.email}]: ", required=False) or item.email
        enrollment_date = read_date("Дата зачисления") or item.enrollment_date

        try:
            updated = self._students_repo.update(
                Student(
                    id=student_id,
                    first_name=first_name,
                    last_name=last_name,
                    direction_id=direction_id,
                    email=email,
                    enrollment_date=enrollment_date,
                )
            )
        except ValueError as exc:
            print(exc)
            pause()
            return
        
        if updated:
            print("Студент обновлён.")
        else:
            print("Не удалось обновить.")
        pause()

    def _delete_direction(self) -> None:
        direction_id = read_int("ID направления: ")
        if direction_id is None:
            return
        if self._directions_repo.delete(direction_id):
            print("Направление удалено.")
        else:
            print("Направление не найдено.")
        pause()

    def _delete_teacher(self) -> None:
        teacher_id = read_int("ID учителя: ")
        if teacher_id is None:
            return
        if self._teachers_repo.delete(teacher_id):
            print("Учитель удален.")
        else:
            print("Учитель не найден.")
        pause()


    def _delete_student(self) -> None:
        student_id = read_int("ID студента: ")
        if student_id is None:
            return
        if self._students_repo.delete(student_id):
            print("Студен удален.")
        else:
            print("Студент не найден.")
        pause()
