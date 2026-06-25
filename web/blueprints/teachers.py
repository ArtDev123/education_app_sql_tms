"""Веб-маршруты учителей."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.entities import Teacher
from web.db import teacher_repo

bp = Blueprint("teachers", __name__, url_prefix="/teachers")


@bp.route("/")
def list_items() -> str:
    items = teacher_repo().get_all()
    return render_template("teachers/list.html", items=items)


@bp.route("/new", methods=["GET", "POST"])
def create() -> str:
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        if not first_name or not last_name or not email or not phone:
            flash("Все поля обязательны.", "error")
        else:
            teacher_repo().add(
                Teacher(
                    id=None,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                )
            )
            flash("Учитель добавлен.", "success")
            return redirect(url_for("teachers.list_items"))
    return render_template("teachers/form.html", item=None)


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
            Teacher(
                id=item.id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )
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
