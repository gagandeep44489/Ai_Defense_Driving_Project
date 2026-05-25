.PHONY: install format lint typecheck test test-verbose train run-api run-ui up down logs clean docker-build

PYTHON ?= python
PIP ?= pip

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

format:
	black .
	isort .

lint:
	flake8 backend frontend data tests

typecheck:
	mypy backend data frontend

test:
	pytest -q

test-verbose:
	pytest -vv --maxfail=1

train:
	$(PYTHON) -m data.generate_data --rows 800 --output data/processed/suppliers.csv
	$(PYTHON) -m backend.models.train

run-api:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

run-ui:
	streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +

docker-build:
	docker compose build
