# GeoSource AI

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-production-009688)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-success)

Enterprise AI-powered supplier intelligence platform for automotive supply chains.

## Features
- ML supplier risk prediction (Low/Medium/High)
- Graph-based alternative supplier recommendations
- NLP news headline risk adjustment
- Explainability payloads for prediction trust
- FastAPI backend + Streamlit dashboard

## Setup
```bash
cp .env.example .env
make install
python -m data.generate_data --rows 800 --output data/processed/suppliers.csv
python -m backend.models.train
make run-api
make run-ui
```

## Architecture
See `docs/architecture/overview.md`.

## API example
```bash
curl -X POST http://localhost:8000/api/v1/predict-risk -H 'Content-Type: application/json' -d '{"supplier":{"country":"US","cost":520,"delivery_time":12,"reliability_score":88,"defect_rate":0.04,"delay_history":2},"headlines":["factory strike causes delay"]}'
```

## Docker
```bash
docker-compose up --build
```
