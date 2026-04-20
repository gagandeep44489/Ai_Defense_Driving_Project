from datetime import datetime, timezone
from time import perf_counter

from fastapi import APIRouter, File, HTTPException, UploadFile

from models.schemas import (
    AlertsResponse,
    DetectAnomalyRequest,
    DetectAnomalyResponse,
    GenerateNotesRequest,
    GenerateNotesResponse,
    RiskScoreRequest,
    RiskScoreResponse,
    SummarizeHistoryRequest,
    SummarizeHistoryResponse,
    UploadAudioResponse,
    WeeklyAnalyticsResponse,
    WorkloadPredictionRequest,
    WorkloadPredictionResponse,
)
from rag.vector_store import vector_store
from services.analytics import aggregate_weekly_data, compute_metrics, generate_insights_with_llm
from services.analytics.event_store import analytics_store
from services.alerts.alert_engine import detect_alerts
from services.anomaly_service import detect_anomalies
from services.history_service import summarize_history
from services.intelligence.risk_scoring import calculate_patient_risk
from services.intelligence.workload_prediction import predict_workload
from services.notes_service import generate_soap_and_prescription
from services.speech_service import speech_service
from utils.compliance import audit_log

router = APIRouter(prefix="/api/v1", tags=["healthcare"])


def _extract_predicted_diseases(text: str) -> list[str]:
    lowered = text.lower()
    disease_keywords = {
        "flu": ["flu", "influenza"],
        "common cold": ["cold", "viral infection"],
        "asthma": ["asthma", "wheezing"],
        "diabetes": ["diabetes", "high glucose"],
        "hypertension": ["hypertension", "high blood pressure"],
    }
    predictions = [name for name, kws in disease_keywords.items() if any(k in lowered for k in kws)]
    return predictions or ["general_follow_up"]


def _extract_symptoms(text: str) -> list[str]:
    lowered = text.lower()
    symptom_keywords = ["fever", "cough", "chest pain", "headache", "fatigue", "breathlessness"]
    return [kw for kw in symptom_keywords if kw in lowered]


@router.post("/upload-audio", response_model=UploadAudioResponse)
async def upload_audio(file: UploadFile = File(...)) -> UploadAudioResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Audio file name missing")

    started = perf_counter()
    try:
        data = await file.read()
        transcript, language = await speech_service.transcribe_audio(data, file.filename)
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="transcription",
            payload={"filename": file.filename, "language": language},
            response_time_ms=elapsed,
            success=True,
        )
        audit_log("upload_audio", {"filename": file.filename, "language": language})
        return UploadAudioResponse(transcript=transcript, language=language)
    except Exception as exc:
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="transcription",
            payload={"filename": file.filename, "error": str(exc)},
            response_time_ms=elapsed,
            success=False,
        )
        raise HTTPException(status_code=500, detail=f"Failed to transcribe audio: {exc}") from exc


@router.post("/generate-notes", response_model=GenerateNotesResponse)
async def generate_notes(payload: GenerateNotesRequest) -> GenerateNotesResponse:
    started = perf_counter()
    try:
        soap_note, prescription = await generate_soap_and_prescription(payload.transcript)
        vector_store.add_document(payload.patient_id, payload.transcript)
        diseases = _extract_predicted_diseases(soap_note + " " + payload.transcript)
        symptoms = _extract_symptoms(payload.transcript)

        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="patient_visit",
            payload={
                "patient_id": payload.patient_id,
                "is_new_patient": payload.patient_id.endswith("001"),
                "consultation_time_minutes": 15,
                "hour_bucket": datetime.now(timezone.utc).strftime("%H:00"),
                "symptoms": symptoms,
            },
            response_time_ms=elapsed,
            success=True,
        )
        analytics_store.log_event(
            event_type="disease_prediction",
            payload={"patient_id": payload.patient_id, "diseases": diseases},
            response_time_ms=elapsed,
            success=True,
        )

        audit_log("generate_notes", {"patient_id": payload.patient_id})
        return GenerateNotesResponse(soap_note=soap_note, prescription_draft=prescription)
    except Exception as exc:
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="patient_visit",
            payload={"patient_id": payload.patient_id, "error": str(exc)},
            response_time_ms=elapsed,
            success=False,
        )
        raise HTTPException(status_code=500, detail=f"Failed to generate notes: {exc}") from exc


@router.post("/summarize-history", response_model=SummarizeHistoryResponse)
async def summarize_history_endpoint(payload: SummarizeHistoryRequest) -> SummarizeHistoryResponse:
    started = perf_counter()
    try:
        summary, context = await summarize_history(payload.patient_id, payload.query)
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="history_summary",
            payload={"patient_id": payload.patient_id},
            response_time_ms=elapsed,
            success=True,
        )
        audit_log("summarize_history", {"patient_id": payload.patient_id, "query": payload.query})
        return SummarizeHistoryResponse(summary=summary, retrieved_context=context)
    except Exception as exc:
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="history_summary",
            payload={"patient_id": payload.patient_id, "error": str(exc)},
            response_time_ms=elapsed,
            success=False,
        )
        raise HTTPException(status_code=500, detail=f"Failed to summarize history: {exc}") from exc


@router.post("/detect-anomaly", response_model=DetectAnomalyResponse)
async def detect_anomaly(payload: DetectAnomalyRequest) -> DetectAnomalyResponse:
    started = perf_counter()
    try:
        anomalies, risk_level = await detect_anomalies(payload.transcript)
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="anomaly_prediction",
            payload={"patient_id": payload.patient_id, "anomalies": anomalies, "risk_level": risk_level},
            response_time_ms=elapsed,
            success=True,
        )
        audit_log("detect_anomaly", {"patient_id": payload.patient_id})
        return DetectAnomalyResponse(anomalies=anomalies, risk_level=risk_level)
    except Exception as exc:
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="anomaly_prediction",
            payload={"patient_id": payload.patient_id, "error": str(exc)},
            response_time_ms=elapsed,
            success=False,
        )
        raise HTTPException(status_code=500, detail=f"Failed to detect anomaly: {exc}") from exc


@router.post("/risk-score", response_model=RiskScoreResponse)
async def risk_score(payload: RiskScoreRequest) -> RiskScoreResponse:
    started = perf_counter()
    try:
        risk_result = await calculate_patient_risk(payload.model_dump())
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="risk_prediction",
            payload={
                "patient_id": payload.patient_id,
                "risk_level": risk_result["risk_level"],
                "score": risk_result["score"],
                "factors": risk_result["factors"],
            },
            response_time_ms=elapsed,
            success=True,
        )
        audit_log("risk_score", {"patient_id": payload.patient_id, "score": risk_result["score"]})
        return RiskScoreResponse(**risk_result)
    except Exception as exc:
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="risk_prediction",
            payload={"patient_id": payload.patient_id, "error": str(exc)},
            response_time_ms=elapsed,
            success=False,
        )
        raise HTTPException(status_code=500, detail=f"Failed to generate risk score: {exc}") from exc


@router.post("/predict-workload", response_model=WorkloadPredictionResponse)
async def predict_doctor_workload(payload: WorkloadPredictionRequest) -> WorkloadPredictionResponse:
    started = perf_counter()
    try:
        workload_result = predict_workload(payload.model_dump())
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="workload_prediction",
            payload={
                "doctor_id": payload.doctor_id,
                "workload_level": workload_result["workload_level"],
                "workload_score": workload_result["workload_score"],
            },
            response_time_ms=elapsed,
            success=True,
        )
        audit_log(
            "predict_workload",
            {
                "patients_per_day": payload.patients_per_day,
                "workload_level": workload_result["workload_level"],
            },
        )
        return WorkloadPredictionResponse(**workload_result)
    except Exception as exc:
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="workload_prediction",
            payload={"doctor_id": payload.doctor_id, "error": str(exc)},
            response_time_ms=elapsed,
            success=False,
        )
        raise HTTPException(status_code=500, detail=f"Failed to predict workload: {exc}") from exc


@router.get("/analytics/weekly", response_model=WeeklyAnalyticsResponse)
async def weekly_analytics(days: int = 7) -> WeeklyAnalyticsResponse:
    started = perf_counter()
    try:
        aggregated = aggregate_weekly_data(days=days)
        metrics = compute_metrics(aggregated)
        insights = await generate_insights_with_llm(metrics)

        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="analytics_report",
            payload={"days": days},
            response_time_ms=elapsed,
            success=True,
        )
        return WeeklyAnalyticsResponse(**metrics, insights=insights)
    except Exception as exc:
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="analytics_report",
            payload={"days": days, "error": str(exc)},
            response_time_ms=elapsed,
            success=False,
        )
        raise HTTPException(status_code=500, detail=f"Failed to generate weekly analytics: {exc}") from exc


@router.get("/alerts", response_model=AlertsResponse)
async def get_alerts() -> AlertsResponse:
    started = perf_counter()
    try:
        alerts = await detect_alerts()
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="alerts_fetch",
            payload={"count": len(alerts)},
            response_time_ms=elapsed,
            success=True,
        )
        return AlertsResponse(alerts=alerts)
    except Exception as exc:
        elapsed = (perf_counter() - started) * 1000
        analytics_store.log_event(
            event_type="alerts_fetch",
            payload={"error": str(exc)},
            response_time_ms=elapsed,
            success=False,
        )
        raise HTTPException(status_code=500, detail=f"Failed to retrieve alerts: {exc}") from exc
