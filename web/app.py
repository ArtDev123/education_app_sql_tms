"""Flask-приложение учебного портала."""

from pathlib import Path

from flask import Flask, render_template

from web.blueprints.directions import bp as directions_bp
from web.blueprints.teachers import bp as teachers_bp
from web.blueprints.courses import bp as courses_bp

from web.db import close_db, init_db

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app() -> Flask:
    """Создать и настроить Flask-приложение."""
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.secret_key = "dev-portal-secret"

    app.before_request(init_db)
    app.teardown_appcontext(close_db)

    app.register_blueprint(directions_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(courses_bp)


    @app.route("/")
    def index() -> str:
        return render_template("index.html")

    return app
