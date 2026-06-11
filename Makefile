.PHONY: help install install-dev lint flake8 mypy run run-cli clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy

help:
	@echo "Доступные команды:"
	@echo "  make install      — создать venv и установить зависимости"
	@echo "  make install-dev  — установить dev-зависимости (flake8, mypy)"
	@echo "  make lint         — запустить flake8"
	@echo "  make typecheck    — проверка типов"
	@echo "  make run          — запустить GUI"
	@echo "  make run-cli      — запустить консольное приложение"
	@echo "  make clean        — удалить кэш Python"

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

install-dev: install
	$(PIP) install -r requirements-dev.txt

typecheck:
	$(MYPY) .

lint:
	$(FLAKE8) .

run:
	$(PYTHON) main.py

run-cli:
	$(PYTHON) main.py --cli

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
