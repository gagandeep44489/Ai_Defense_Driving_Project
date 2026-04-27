# GeoSource AI

## Project Overview
GeoSource AI is an AI-powered supplier intelligence platform for automotive supply chains. It predicts supplier risk (Low/Medium/High), recommends alternative suppliers, explains model decisions, and augments risk with NLP-based external news signals.

## Problem Statement
Automotive OEMs rely on complex multi-country supplier networks. Disruptions from delays, quality issues, and external events can stop production. Decision teams need a fast, explainable, and data-driven tool to identify risky suppliers and switch to robust alternatives.

## Solution
GeoSource AI combines four intelligence layers:
1. **ML Risk Prediction** using supplier operational features.
2. **Graph Intelligence** to detect supplier similarity communities.
3. **Explainable AI (SHAP)** for feature-level prediction reasoning.
4. **NLP Risk Signals** from external news headlines.

## Advanced AI Features

### Graph Intelligence
- Builds a supplier graph with `NetworkX`:
  - Nodes: suppliers
  - Edges: same country, similar cost, similar reliability
- Detects supplier communities (clusters).
- Uses graph-aware embeddings/centrality to improve top-3 recommendation quality.

### Explainable AI
- Integrates SHAP (with graceful fallback) to explain prediction contributions.
- Returns per-feature impacts for each prediction.
- Frontend displays top feature impacts as a bar chart.

### NLP Integration
- News headline sentiment module (`backend/nlp_risk.py`) produces a risk adjustment score.
- Final risk combines model score + NLP score.
- API returns headline-level sentiment and summary signal.

## Features
- Synthetic dataset generator (`600` rows default).
- FastAPI endpoints:
  - `POST /predict-risk`
  - `POST /recommend`
  - `GET /graph-summary`
- Streamlit dashboard:
  - supplier selector,
  - news headline input,
  - model/final risk metrics,
  - explainability chart,
  - top-3 recommendations,
  - local supplier graph visualization.

## Tech Stack
- Python
- pandas, numpy
- scikit-learn, xgboost
- FastAPI, Uvicorn
- Streamlit
- NetworkX
- SHAP
- Matplotlib

## Project Structure
```text
geosource-ai/
│── data/
│   │── generate_data.py
│   │── suppliers.csv
│── models/
│   │── .gitkeep  # model artifact generated after training (risk_model.pkl)
│── backend/
│   │── __init__.py
│   │── main.py
│   │── risk_model.py
│   │── recommendation.py
│   │── graph_model.py
│   │── explainability.py
│   │── nlp_risk.py
│── frontend/
│   │── app.py
│── notebooks/
│   │── .gitkeep
│── requirements.txt
│── README.md
```

## How to Run Locally

### 1) Clone and enter project
```bash
git clone <your-repo-url>
cd geosource-ai
```

### 2) Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 3) Generate synthetic data
```bash
python data/generate_data.py
```

### 4) Train and save risk model
```bash
python backend/risk_model.py
```
This generates `models/risk_model.pkl`.

### 5) Start FastAPI backend
```bash
uvicorn backend.main:app --reload --port 8000
```

### 6) Start Streamlit dashboard (new terminal)
```bash
streamlit run frontend/app.py
```

## API Examples

### Predict Risk + NLP + Explainability
```bash
curl -X POST "http://127.0.0.1:8000/predict-risk" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "Germany",
    "cost": 110,
    "delivery_time": 16,
    "reliability_score": 82,
    "defect_rate": 2.8,
    "delay_history": 6,
    "headlines": [
      "Port delay affects regional shipments",
      "Supplier wins innovation award"
    ]
  }'
```

### Recommend Alternatives
```bash
curl -X POST "http://127.0.0.1:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{"supplier_id": "SUP-0001"}'
```

### Graph Summary
```bash
curl "http://127.0.0.1:8000/graph-summary"
```

## Screenshots
> Add dashboard screenshots here.
- `docs/images/dashboard-overview.png`
- `docs/images/risk-explanation.png`
- `docs/images/supplier-graph.png`

## Future Improvements
- Replace synthetic data with ERP + logistics event streams.
- Add online learning/model drift monitoring.
- Add true Node2Vec/GraphSAGE embeddings.
- Add RAG-based geopolitical risk context from live sources.
- Add auth, RBAC, audit logs, and deployment manifests.
