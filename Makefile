# Simple make helper for common tasks

.PHONY: help install dev-install lint format test precommit

help:
	@echo "make install         # Install runtime requirements"
	@echo "make dev-install     # Install dev requirements (formatters, linters)"
	@echo "make lint            # Run linters"
	@echo "make format          # Run formatters"
	@echo "make test            # Run tests"
	@echo "make precommit       # Run pre-commit hooks"

install:
	python -m pip install -r requirements.txt

dev-install:
	python -m pip install -r requirements-dev.txt

lint:
	black --check .
	isort --check-only .
	flake8

format:
	black .
	isort .

test:
	pytest -q

precommit:
	pre-commit run --all-files
