#!/usr/bin/env python3
"""Точка входа в приложение учебного портала."""

import argparse

from cli.menu import PortalApp
from database.connection import Database


def run_cli() -> None:
    """Запустить консольный интерфейс."""
    with Database() as db:
        app = PortalApp(db)
        app.run()


def run_web() -> None:
    """Запустить веб-интерфейс Flask."""
    from web.app import create_app

    app = create_app()
    app.run(debug=True)


def main() -> None:
    """Запустить приложение в выбранном режиме."""
    parser = argparse.ArgumentParser(description="Учебный портал")
    parser.add_argument("--web", action="store_true", help="запустить веб-интерфейс")
    parser.add_argument(
        "--cli", action="store_true", help="запустить консольный интерфейс"
    )
    args = parser.parse_args()

    if args.web:
        run_web()
    else:
        run_cli()


if __name__ == "__main__":
    main()
