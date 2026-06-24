.PHONY: help install install-dev lint typecheck run run-cli clean

VENV := venv
# На Windows исполняемые файлы лежат в папе Scripts, и они имеют расширение .exe
PYTHON := $(VENV)\Scripts\python.exe
PIP := $(VENV)\Scripts\pip.exe
FLAKE8 := $(VENV)\Scripts\flake8.exe
MYPY := $(VENV)\Scripts\mypy.exe

help:
	@echo Доступные команды:
	@echo   make install      - создать venv и установить зависимости
	@echo   make install-dev  - установить dev-зависимости (flake8, mypy)
	@echo   make lint         - запустить flake8
	@echo   make typecheck    - проверка типов
	@echo   make run          - запустить веб-интерфейс
	@echo   make run-cli      - запустить консольное приложение
	@echo   make run-web      - запустить веб-интерфейс Flask
	@echo   make clean        - удалить кэш Python

install:
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt

install-dev: install
	$(PIP) install -r requirements-dev.txt

typecheck:
	$(PYTHON) -m mypy .

lint:
	$(PYTHON) -m flake8 .

run:
	$(PYTHON) main.py --web

run-cli:
	$(PYTHON) main.py --cli

run-web:
	$(PYTHON) main.py --web

clean:
	@if exist .mypy_cache rmdir /s /q .mypy_cache
	@for /d /r . %%i in (__pycache__) do @if exist "%%i" rmdir /s /q "%%i"
	@del /s /q /f *.pyc 2>nul || (exit 0)
