"""API schemas for supplier workflows."""
from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field


class SupplierFeatures(BaseModel):
    supplier_id: str | None = None
    country: str
    cost: float
    delivery_time: float
    reliability_score: float = Field(ge=0, le=100)
    defect_rate: float = Field(ge=0, le=1)
    delay_history: int = Field(ge=0)


class PredictRequest(BaseModel):
    supplier: SupplierFeatures
    headlines: List[str] = Field(default_factory=list)


class NLPSignal(BaseModel):
    sentiment: float
    risk_adjustment: float
    summary: str


class PredictResponse(BaseModel):
    risk_level: str
    confidence: float
    risk_score: float
    nlp_signal: NLPSignal
    explanation: Dict[str, List[Dict[str, float | str]]]


class RecommendRequest(BaseModel):
    supplier_id: str
    top_k: int = 3


class Recommendation(BaseModel):
    supplier_id: str
    score: float
    country: str
    risk_level: str


class RecommendResponse(BaseModel):
    alternatives: List[Recommendation]
