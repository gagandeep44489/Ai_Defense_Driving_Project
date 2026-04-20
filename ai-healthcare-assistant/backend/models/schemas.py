from typing import Literal
from pydantic import BaseModel, Field


class UploadAudioResponse(BaseModel):
    transcript: str
    language: Literal["en", "hi", "mixed"]


class GenerateNotesRequest(BaseModel):
    patient_id: str
    transcript: str


class GenerateNotesResponse(BaseModel):
    soap_note: str
    prescription_draft: str


class SummarizeHistoryRequest(BaseModel):
    patient_id: str
    query: str = Field(default="Summarize recent history")


class SummarizeHistoryResponse(BaseModel):
    summary: str
    retrieved_context: list[str]


class DetectAnomalyRequest(BaseModel):
    patient_id: str
    transcript: str


class DetectAnomalyResponse(BaseModel):
    anomalies: list[str]
    risk_level: Literal["low", "medium", "high"]


class RiskScoreRequest(BaseModel):
    patient_id: str
    symptoms: list[str] = Field(default_factory=list)
    medical_history: list[str] = Field(default_factory=list)
    visits_last_90_days: int = 0
    anomalies: list[str] = Field(default_factory=list)


class RiskScoreResponse(BaseModel):
    risk_level: Literal["Low", "Medium", "High"]
    score: int
    explanation: str
    label: str
    factors: list[str]


class WorkloadPredictionRequest(BaseModel):
    doctor_id: str = "doctor-001"
    patients_per_day: int
    average_consultation_minutes: float
    complexity_score: float


class WorkloadPredictionResponse(BaseModel):
    workload_level: Literal["Low", "Medium", "High"]
    workload_score: float
    complexity_factor: float
    suggested_actions: list[str]
    label: str


class WeeklyAnalyticsResponse(BaseModel):
    patient_stats: dict
    risk_distribution: dict
    disease_trends: dict
    workload_summary: dict
    system_metrics: dict
    insights: str


class AlertItem(BaseModel):
    alert_id: str
    type: str
    severity: Literal["Critical", "High", "Medium", "Low"]
    priority_score: float
    message: str
    recommendation: str
    timestamp: str


class AlertsResponse(BaseModel):
    alerts: list[AlertItem]


class ErrorResponse(BaseModel):
    detail: str
