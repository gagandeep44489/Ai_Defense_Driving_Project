.PHONY: dev api web test lint migrate docker-up docker-down

dev: docker-up
api:
	cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
web:
	cd apps/web && npm run dev
test:
	cd apps/api && pytest
	cd apps/web && npm test
lint:
	cd apps/api && ruff check app tests && mypy app
	cd apps/web && npm run lint
migrate:
	cd apps/api && alembic upgrade head
docker-up:
	docker compose up --build
docker-down:
	docker compose down -v
