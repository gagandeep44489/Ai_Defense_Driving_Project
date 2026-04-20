from __future__ import annotations

from dataclasses import dataclass

from rag.vector_store import vector_store
from services.llm_service import llm_service
from utils.config import settings

SEVERE_SYMPTOMS = {
    "chest pain",
    "shortness of breath",
    "severe bleeding",
    "fainting",
    "high fever",
    "confusion",
    "seizure",
}

CHRONIC_KEYWORDS = {
    "diabetes",
    "hypertension",
    "asthma",
    "copd",
    "heart disease",
    "kidney disease",
    "cancer",
}


@dataclass
class RiskScoreBreakdown:
    score: int
    reasons: list[str]


class RiskModelPlaceholder:
    """Future ML model placeholder for learned risk predictions."""

    def predict_delta(self, _: dict) -> int:
        return 0


def _has_keyword(text_items: list[str], keywords: set[str]) -> bool:
    merged = " ".join(text_items).lower()
    return any(keyword in merged for keyword in keywords)


def _rule_based_score(
    symptoms: list[str],
    history: list[str],
    visits_last_90_days: int,
    anomalies: list[str],
) -> RiskScoreBreakdown:
    score = 0
    reasons: list[str] = []

    if _has_keyword(symptoms, SEVERE_SYMPTOMS):
        score += 3
        reasons.append("severe_symptoms(+3)")

    if _has_keyword(history, CHRONIC_KEYWORDS):
        score += 2
        reasons.append("chronic_history(+2)")

    if visits_last_90_days >= 3:
        score += 1
        reasons.append("frequent_visits(+1)")

    if anomalies:
        score += 2
        reasons.append("detected_anomaly(+2)")

    return RiskScoreBreakdown(score=score, reasons=reasons)


def _score_to_level(score: int) -> str:
    if score >= 6:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


async def _generate_explanation(
    level: str,
    score: int,
    reasons: list[str],
    context_chunks: list[str],
) -> str:
    prompt = f"""
Create a short, neutral explanation for an AI-assisted patient risk score.
Rules:
- Start with: 'AI-assisted insights:'
- Do not provide diagnosis or medical advice.
- Mention key factors from reasons.

Risk level: {level}
Score: {score}
Reasons: {', '.join(reasons) if reasons else 'no major risk signals'}
Context snippets: {' | '.join(context_chunks) if context_chunks else 'none'}
""".strip()

    explanation = await llm_service.generate_text(prompt, temperature=0.1)
    if not explanation.lower().startswith("ai-assisted insights"):
        explanation = f"AI-assisted insights: {explanation}"
    return explanation


async def calculate_patient_risk(payload: dict) -> dict:
    symptoms: list[str] = payload.get("symptoms", [])
    history: list[str] = payload.get("medical_history", [])
    visits_last_90_days: int = payload.get("visits_last_90_days", 0)
    anomalies: list[str] = payload.get("anomalies", [])
    patient_id: str = payload.get("patient_id", "")

    rag_context = vector_store.query(
        patient_id=patient_id,
        query_text="risk factors and recent encounters",
        top_k=settings.vector_top_k,
    )

    rule = _rule_based_score(symptoms, history + rag_context, visits_last_90_days, anomalies)

    model = RiskModelPlaceholder()
    ml_delta = model.predict_delta(payload)
    total_score = max(0, rule.score + ml_delta)
    risk_level = _score_to_level(total_score)

    explanation = await _generate_explanation(risk_level, total_score, rule.reasons, rag_context)

    return {
        "risk_level": risk_level,
        "score": total_score,
        "explanation": explanation,
        "label": "AI-assisted insights",
        "factors": rule.reasons,
    }
