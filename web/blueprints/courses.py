"""Веб-маршруты курсов."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.entities import Course
from web.db import teacher_repo, course_repo, direction_repo
from utils import is_valid_int

bp = Blueprint("courses", __name__, url_prefix="/courses")


@bp.route("/")
def list_items() -> str:
    items = course_repo().get_all()
    return render_template("courses/list.html", items=items)


@bp.route("/new", methods=["GET", "POST"])
def create() -> str:
    directions = direction_repo().get_all()
    teachers = teacher_repo().get_all()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        direction_id = request.form.get("direction_id", "").strip()
        teacher_id = request.form.get("teacher_id", "").strip()
        if not name:
            flash("Имя обязательно.", "error")
        elif not is_valid_int(direction_id):
            flash("ID направления некорректный.", "error")
        elif teacher_id and not is_valid_int(teacher_id):
            flash("ID учителя некорректный.", "error")
        else:
            course_repo().add(Course(id=None, name= name, direction_id=direction_id, teacher_id=teacher_id))
            flash("Курс добавлен.", "success")
            return redirect(url_for("couses.list_items"))
    return render_template("courses/form.html", item=None, directions = directions, teachers = teachers)


@bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
def edit(item_id: int) -> str:
    item = teacher_repo().get_by_id(item_id)
    if item is None:
        flash("Направление не найдено.", "error")
        return redirect(url_for("directions.list_items"))
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        if not first_name or not last_name or not email or not phone:
            flash("Все поля обязательны.", "error")
        elif teacher_repo().update(
            Teacher(id=item.id, first_name= first_name, last_name= last_name, email= email, phone= phone)
        ):
            flash("Учитель обновлен.", "success")
            return redirect(url_for("teachers.list_items"))
        else:
            flash("Не удалось обновить.", "error")
    return render_template("teachers/form.html", item=item)


@bp.post("/<int:item_id>/delete")
def delete(item_id: int) -> str:
    if teacher_repo().delete(item_id):
        flash("Учитель удален.", "success")
    else:
        flash("Учитель не найден.", "error")
    return redirect(url_for("teachers.list_items"))
