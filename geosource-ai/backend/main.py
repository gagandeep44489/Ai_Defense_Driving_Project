"""FastAPI service for risk prediction, explainability, NLP signals, and recommendations."""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

from backend.explainability import explain_prediction
from backend.nlp_risk import combine_model_and_news_risk, news_risk_score
from backend.risk_model import predict_risk
from backend.recommendation import recommend_alternatives
from backend.graph_model import load_graph_artifacts


app = FastAPI(title="GeoSource AI API", version="2.0.0")


class SupplierInput(BaseModel):
    country: str = Field(..., examples=["Germany"])
    cost: float = Field(..., ge=0)
    delivery_time: float = Field(..., ge=0)
    reliability_score: float = Field(..., ge=0, le=100)
    defect_rate: float = Field(..., ge=0)
    delay_history: int = Field(..., ge=0)
    headlines: List[str] = Field(default_factory=list)


class RecommendInput(BaseModel):
    supplier_id: str


@app.get("/")
def health() -> dict:
    return {"status": "ok", "service": "GeoSource AI", "version": "2.0.0"}


@app.post("/predict-risk")
def predict_supplier_risk(payload: SupplierInput) -> dict:
    features = payload.model_dump(exclude={"headlines"})
    model_risk = predict_risk(features)

    nlp = news_risk_score(payload.headlines)
    fused = combine_model_and_news_risk(model_risk, nlp["news_risk"])
    explanation = explain_prediction(features)

    return {
        "model_risk": model_risk,
        "final_risk": fused["final_risk"],
        "model_score": fused["model_score"],
        "news_risk": nlp["news_risk"],
        "combined_score": fused["combined_score"],
        "news_summary": nlp["summary"],
        "headline_scores": nlp["headline_scores"],
        "feature_explanations": explanation,
    }


@app.post("/recommend")
def recommend(payload: RecommendInput) -> dict:
    try:
        recs = recommend_alternatives(payload.supplier_id, top_k=3)
        return {"supplier_id": payload.supplier_id, "alternatives": recs}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/graph-summary")
def graph_summary() -> dict:
    artifacts = load_graph_artifacts()
    return {
        "nodes": artifacts.graph.number_of_nodes(),
        "edges": artifacts.graph.number_of_edges(),
        "clusters": len(set(artifacts.clusters.values())),
    }


# Run with: uvicorn backend.main:app --reload --port 8000
