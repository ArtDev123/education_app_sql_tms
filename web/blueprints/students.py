"""Веб-маршруты студентов."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.entities import Student
from web.db import direction_repo, student_repo
from utils import is_valid_int
from repositories.base import parse_date

bp = Blueprint("students", __name__, url_prefix="/students")


@bp.route("/")
def list_items() -> str:
    items = student_repo().get_all()
    return render_template("students/list.html", items=items)


@bp.route("/new", methods=["GET", "POST"])
def create() -> str:
    directions = direction_repo().get_all()
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        direction_id = request.form.get("direction_id", "").strip()
        email = request.form.get("email", "").strip()
        enrollment_date = parse_date(request.form.get("enrollment_date", "").strip())
        if not first_name or not last_name or not email:
            flash("ФИО, e-mail обязательны!", "error")
        elif not is_valid_int(direction_id):
            flash("Не валидное направление", "error")

        else:
            student_repo().add(
                Student(
                    id=None,
                    first_name=first_name,
                    last_name=last_name,
                    direction_id=direction_id,
                    email=email,
                    enrollment_date=enrollment_date,
                )
            )
            flash("Студент добавлен.", "success")
            return redirect(url_for("students.list_items"))
    return render_template("students/form.html", item=None, directions = directions)


@bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
def edit(item_id: int) -> str:
    directions = direction_repo().get_all()
    item = student_repo().get_by_id(item_id)
    if item is None:
        flash("Студент не найден.", "error")
        return redirect(url_for("students.list_items"))
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        direction_id = request.form.get("direction_id", "").strip()
        email = request.form.get("email", "").strip()
        enrollment_date = parse_date(request.form.get("enrollment_date", "").strip())
        if not first_name or not last_name or not email:
            flash("ФИО, e-mail обязательны!", "error")
        elif not is_valid_int(direction_id):
            flash("Не валидное направление", "error")
        elif student_repo().update(
            Student(
                id=item.id,
                first_name=first_name,
                last_name=last_name,
                direction_id=direction_id,
                email=email,
                enrollment_date=enrollment_date,
            )
        ):
            flash("Студент обновлен.", "success")
            return redirect(url_for("students.list_items"))
        else:
            flash("Не удалось обновить.", "error")
    return render_template("students/form.html", item=item, directions=directions)


@bp.post("/<int:item_id>/delete")
def delete(item_id: int) -> str:
    if student_repo().delete(item_id):
        flash("Студент удален.", "success")
    else:
        flash("Студент не найден.", "error")
    return redirect(url_for("students.list_items"))
