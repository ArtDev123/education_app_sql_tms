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
            course_repo().add(
                Course(
                    id=None, name=name, direction_id=direction_id, teacher_id=teacher_id
                )
            )
            flash("Курс добавлен.", "success")
            return redirect(url_for("courses.list_items"))
    return render_template(
        "courses/form.html", item=None, directions=directions, teachers=teachers
    )


@bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
def edit(item_id: int) -> str:
    directions = direction_repo().get_all()
    teachers = teacher_repo().get_all()
    item = course_repo().get_by_id(item_id)
    if item is None:
        flash("Курс не найден.", "error")
        return redirect(url_for("courses.list_items"))
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
        elif course_repo().update(
            Course(
                id=item.id, name=name, direction_id=direction_id, teacher_id=teacher_id
            )
        ):
            flash("Курс обновлен.", "success")
            return redirect(url_for("courses.list_items"))
        else:
            flash("Не удалось. ", "error")
    return render_template(
        "courses/form.html", item=item, directions=directions, teachers=teachers
    )


@bp.post("/<int:item_id>/delete")
def delete(item_id: int) -> str:
    if course_repo().delete(item_id):
        flash("Курс удален.", "success")
    else:
        flash("Курс не найден.", "error")
    return redirect(url_for("courses.list_items"))
