"""Веб-маршруты направлений."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.entities import StudentResult
from web.db import results_repo, student_repo, course_repo
from utils import is_valid_int
from repositories.base import parse_date

bp = Blueprint("results", __name__, url_prefix="/results")


@bp.route("/")
def list_items() -> str:
    items = results_repo().get_all()
    return render_template("results/list.html", items=items)


@bp.route("/new", methods=["GET", "POST"])
def create() -> str:
    students = student_repo().get_all()
    courses = course_repo().get_all()
    if request.method == "POST":
        course_id = request.form.get("course_id", "").strip()
        student_id = request.form.get("student_id", "").strip()
        grade = request.form.get("grade", "").strip()
        exam_date = parse_date(request.form.get("exam_date", "").strip())
        if not is_valid_int(student_id):
            flash("ID студента некорректный.", "error")
        elif not is_valid_int(course_id):
            flash("ID курса некорректный.", "error")
        elif not is_valid_int(grade):
            flash("Оценка некорректная.", "error")
        else:
            results_repo().add(StudentResult(
            id=None,
            student_id=student_id,
            course_id=course_id,
            grade=int(grade),
            exam_date=exam_date,
        ))
            flash("Оценка добавлена.", "success")
            return redirect(url_for("results.list_items"))
    return render_template("results/form.html", item=None, students=students, courses=courses)


@bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
def edit(item_id: int) -> str:
    students = student_repo().get_all()
    courses = course_repo().get_all()
    item = results_repo().get_by_id(item_id)
    if item is None:
        flash("Оценка не найдена.", "error")
        return redirect(url_for("results.list_items"))
    if request.method == "POST":
        course_id = request.form.get("course_id", "").strip()
        student_id = request.form.get("student_id", "").strip()
        grade = request.form.get("grade", "").strip()
        exam_date = parse_date(request.form.get("exam_date", "").strip())
        if not is_valid_int(student_id):
            flash("ID студента некорректный.", "error")
        elif not is_valid_int(course_id):
            flash("ID курса некорректный.", "error")
        elif not is_valid_int(grade):
            flash("Оценка некорректная.", "error")
        elif results_repo().update(StudentResult(
            id=item_id,
            student_id=student_id,
            course_id=course_id,
            grade=int(grade),
            exam_date=exam_date,
        )):
            flash("Оценка обновлена.", "success")
            return redirect(url_for("results.list_items"))
        else:
            flash("Не удалось обновить.", "error")
    return render_template("results/form.html", students=students, courses=courses, item=item)


@bp.post("/<int:item_id>/delete")
def delete(item_id: int) -> str:
    if results_repo().delete(item_id):
        flash("Направление удалено.", "success")
    else:
        flash("Направление не найдено.", "error")
    return redirect(url_for("directions.list_items"))
