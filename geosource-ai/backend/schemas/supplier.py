"""API schemas for supplier risk prediction and recommendations."""
from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field


class SupplierFeatures(BaseModel):
    supplier_id: str | None = None
    country: str = Field(min_length=2, max_length=3)
    cost: float = Field(gt=0)
    delivery_time: float = Field(gt=0)
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
    confidence: float = Field(ge=0, le=1)
    risk_score: float = Field(ge=0, le=1)
    nlp_signal: NLPSignal
    explanation: Dict[str, List[Dict[str, float | str]]]


class RecommendRequest(BaseModel):
    supplier_id: str
    top_k: int = Field(default=3, ge=1, le=10)


class Recommendation(BaseModel):
    supplier_id: str
    score: float
    country: str
    risk_level: str


class RecommendResponse(BaseModel):
    alternatives: List[Recommendation]


class HealthResponse(BaseModel):
    status: str
    service: str
    model_loaded: bool
