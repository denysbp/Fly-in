PY := python3
PACKAGE := src/


install_venv:
	$(PY) -m venv .venv

install: requirements.txt
	pip install -r requirements.txt

debug:
	$(PY) -m pdb

lint:
	$(PY) -m flake8 . && python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PY) -m flake8 . && python3 -m mypy . --strict

clean:
	rm -rf $(PACKAGE)__pycache__
	rm -rf __pycache__