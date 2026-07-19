PY := python3
PACKAGE := src/
MAP ?= ./maps/easy/01_linear_path.txt
TEST ?=
MODELS := $(PACKAGE)models/
VISUALIZATION := $(PACKAGE)visualization/
VENV := .venv


VENV_PY := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip

all: run

$(VENV)/bin/activate: requirements.txt
	@echo "Creating venv..."
	$(PY) -m venv $(VENV)
	@echo "Installing dependencies..."
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt
	@touch $(VENV)/bin/activate

isolation: $(VENV)/bin/activate

run: isolation
	@PYGAME_HIDE_SUPPORT_PROMPT=1 $(VENV_PY) fly-in.py $(MAP) $(TEST)

render: isolation
	@PYGAME_HIDE_SUPPORT_PROMPT=1 $(VENV_PY) fly-in.py $(MAP) --visualizer

install: $(VENV)/bin/activate
	@$(VENV_PIP) install -r requirements.txt

test: isolation
	@PYGAME_HIDE_SUPPORT_PROMPT=1 $(VENV_PY) test.py

debug: isolation
	$(VENV_PY) -m pdb

lint: isolation
	$(VENV_PY) -m flake8 . && $(VENV_PY) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


clean:
	rm -rf $(PACKAGE)__pycache__
	rm -rf $(MODELS)__pycache__
	rm -rf $(VISUALIZATION)__pycache__
	rm -rf __pycache__
	rm -rf .mypy_cache



.PHONY: isolation run install debug lint lint-strict clean render all test