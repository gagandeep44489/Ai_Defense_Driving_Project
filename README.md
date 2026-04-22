# AI Trust Score Dashboard

Production-ready full-stack application that estimates a company trust score (0–100) from multiple signals.

## Project Structure

```text
/backend
  /controllers
  /services
  /models
  /routes
  /utils
  /config
/frontend
  /components
  /pages
  /services
  /hooks
```

## Features

- Input accepts company names or website URLs.
- Modular backend services:
  - SocialSignalService
  - ReviewSentimentService
  - WebsiteQualityService
  - NewsAnalysisService
- Configurable weighted trust scoring engine.
- Risk level classification: Safe, Moderate, Risky.
- "Why this score?" explanation generator.
- Dashboard UI with cards, mini-bars, insights, loading and error states.

## API

### `POST /analyze`

Request:

```json
{
  "input": "openai.com"
}
```

Response example:

```json
{
  "trustScore": 79,
  "riskLevel": "Safe",
  "signals": {
    "social": 60,
    "reviews": 65,
    "website": 80,
    "news": 75
  },
  "insights": [
    "Social presence indicates limited brand legitimacy.",
    "Review sentiment shows 0 positive cues and 0 risk cues.",
    "Website quality checks suggest healthy technical trust indicators.",
    "Recent coverage around \"openai.com\" is mostly positive. Financial/news sentiment model indicates manageable external risk."
  ],
  "explanation": "This score is 79/100 (Safe) because website is strongest at 80, while social is weakest at 60."
}
```

## SOLID Architecture Decisions

- **Single Responsibility**: each signal service owns one domain only.
- **Open/Closed**: scoring algorithm is behind a `ScoringStrategy` abstraction.
- **Liskov Substitution**: all signal services conform to `BaseSignalService#analyze` contract.
- **Interface Segregation**: services expose focused methods (`analyze`, `calculate`, `generate`).
- **Dependency Inversion**: `TrustScoreEngine` receives dependencies through container-based injection.

## Local Run Instructions

### 1) Backend

```bash
cd backend
npm install
cp .env.example .env
npm run dev
```

Backend runs at `http://localhost:4000`.

### 2) Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Environment Variables

### `backend/.env.example`

- `PORT=4000`
- `CORS_ORIGIN=http://localhost:5173`
- `WEIGHT_SOCIAL=0.25`
- `WEIGHT_REVIEWS=0.30`
- `WEIGHT_WEBSITE=0.25`
- `WEIGHT_NEWS=0.20`

### `frontend/.env.example`

- `VITE_API_BASE_URL=http://localhost:4000`

## Notes

Current services are mock-friendly and deterministic for hackathon delivery. You can replace each service implementation with real integrations without changing API contracts.
