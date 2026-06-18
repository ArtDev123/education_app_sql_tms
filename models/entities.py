"""Модели данных учебного портала."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Direction:
    """Учебное направление."""

    id: Optional[int]
    name: str
    description: str = ""


@dataclass
class Teacher:
    """Преподаватель."""

    id: Optional[int]
    first_name: str
    last_name: str
    email: str = ""
    phone: str = ""


@dataclass
class Course:
    """Курс."""

    id: Optional[int]
    name: str
    direction_id: int
    teacher_id: Optional[int] = None


@dataclass
class Student:
    """Студент."""

    id: Optional[int]
    first_name: str
    last_name: str
    direction_id: int
    email: str = ""
    enrollment_date: Optional[date] = None


@dataclass
class StudentResult:
    """Результат (оценка) студента по курсу."""

    id: Optional[int]
    student_id: int
    course_id: int
    grade: float
    exam_date: Optional[date] = None
