"""Веб-маршруты направлений."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.entities import Direction
from web.db import direction_repo

bp = Blueprint("directions", __name__, url_prefix="/directions")


@bp.route("/")
def list_items() -> str:
    items = direction_repo().get_all()
    return render_template("directions/list.html", items=items)


@bp.route("/new", methods=["GET", "POST"])
def create() -> str:
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if not name:
            flash("Название обязательно.", "error")
        else:
            direction_repo().add(Direction(id=None, name=name, description=description))
            flash("Направление добавлено.", "success")
            return redirect(url_for("directions.list_items"))
    return render_template("directions/form.html", item=None)


@bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
def edit(item_id: int) -> str:
    item = direction_repo().get_by_id(item_id)
    if item is None:
        flash("Направление не найдено.", "error")
        return redirect(url_for("directions.list_items"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if not name:
            flash("Название обязательно.", "error")
        elif direction_repo().update(
            Direction(id=item.id, name=name, description=description)
        ):
            flash("Направление обновлено.", "success")
            return redirect(url_for("directions.list_items"))
        else:
            flash("Не удалось обновить.", "error")
    return render_template("directions/form.html", item=item)


@bp.post("/<int:item_id>/delete")
def delete(item_id: int) -> str:
    if direction_repo().delete(item_id):
        flash("Направление удалено.", "success")
    else:
        flash("Направление не найдено.", "error")
    return redirect(url_for("directions.list_items"))
