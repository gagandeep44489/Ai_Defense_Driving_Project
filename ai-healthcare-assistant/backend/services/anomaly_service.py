from services.llm_service import llm_service
from services.prompts import ANOMALY_PROMPT_TEMPLATE


async def detect_anomalies(transcript: str) -> tuple[list[str], str]:
    result = await llm_service.generate_json(ANOMALY_PROMPT_TEMPLATE.format(transcript=transcript))
    anomalies = result.get("anomalies", [])
    if not isinstance(anomalies, list):
        anomalies = ["Malformed anomaly output"]

    risk_level = result.get("risk_level", "medium")
    if risk_level not in {"low", "medium", "high"}:
        risk_level = "medium"

    return anomalies, risk_level
