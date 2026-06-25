"""Вспомогательные функции для консольного интерфейса."""

from datetime import date
from typing import Optional


def read_input(prompt: str, required: bool = True) -> str:
    """Считать строку от пользователя."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("Поле обязательно для заполнения.")


def read_int(prompt: str, required: bool = True) -> Optional[int]:
    """Считать целое число от пользователя."""
    while True:
        value = read_input(prompt, required=required)
        if not value and not required:
            return None
        try:
            return int(value)
        except ValueError:
            print("Введите целое число.")


def read_float(prompt: str) -> float:
    """Считать число с плавающей точкой от пользователя."""
    while True:
        value = read_input(prompt)
        try:
            number = float(value.replace(",", "."))
            return number
        except ValueError:
            print("Введите число.")


def read_date(prompt: str, required: bool = False) -> Optional[date]:
    """Считать дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = read_input(
            f"{prompt} (ГГГГ-ММ-ДД, Enter — пропустить): ",
            required=required,
        )
        if not value:
            return None
        try:
            return date.fromisoformat(value)
        except ValueError:
            print("Неверный формат даты. Используйте ГГГГ-ММ-ДД.")


def pause() -> None:
    """Пауза перед возвратом в меню."""
    input("\nНажмите Enter для продолжения...")
