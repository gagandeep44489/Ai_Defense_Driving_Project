# ClimateShield AI Recommendation Engine

Production-ready FastAPI service for personalized climate adaptation recommendations.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker

```bash
docker compose up --build
```

## Endpoints

- `POST /recommendations`
- `POST /bulk-recommendations`
- `GET /recommendations/{location}`
- `GET /health`
- `GET /metrics`

## Architecture

Clean Architecture separates domain entities, repository interfaces, use cases, infrastructure adapters, and FastAPI interfaces. Recommendation behavior is extended by adding a new `RecommendationStrategy` and registering it in the factory.
