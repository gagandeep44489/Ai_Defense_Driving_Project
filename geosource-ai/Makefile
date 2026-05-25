.PHONY: install format lint test train run-api run-ui

install:
	pip install -r requirements.txt

format:
	black .
	isort .

lint:
	flake8 backend frontend data tests
	mypy backend data

test:
	pytest -q

train:
	python -m data.generate_data --rows 800 --output data/processed/suppliers.csv
	python -m backend.models.train

run-api:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

run-ui:
	streamlit run frontend/app.py --server.port 8501
