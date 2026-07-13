# ClimateShield AI

ClimateShield AI contains a FastAPI recommendation engine and a React dashboard for climate adaptation planning.

## Backend

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend endpoints:

- `POST /recommendations`
- `POST /bulk-recommendations`
- `GET /recommendations/{location}`
- `GET /health`
- `GET /metrics`

## Frontend Dashboard

The dashboard lives in `climateshield-dashboard/` and consumes the backend at `VITE_API_BASE_URL`.

```bash
cd climateshield-dashboard
cp .env.example .env
npm install
npm run dev
```

Dashboard URL: `http://localhost:3000`.

## Architecture

Clean Architecture separates backend domain entities, repository interfaces, use cases, infrastructure adapters, and FastAPI interfaces. The frontend uses a feature-based React structure with UI components, TanStack Query hooks, repository interfaces, and an Axios HTTP client.
