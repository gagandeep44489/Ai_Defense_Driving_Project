from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from services.alerts.alert_rules import detect_alerts_from_rules
from services.alerts.prioritizer import rank_alerts
from services.analytics import aggregate_weekly_data, compute_metrics
from services.llm_service import llm_service


async def _explain_alert(alert: dict) -> tuple[str, str]:
    prompt = f"""
Explain this alert and suggest an actionable step for a doctor/admin.
Keep tone calm, practical, and avoid diagnostic language.

Alert:
- Type: {alert.get('type')}
- Severity: {alert.get('severity')}
- Priority score: {alert.get('priority_score')}
- Message: {alert.get('message')}
""".strip()

    text = await llm_service.generate_text(prompt, temperature=0.2)
    if text.startswith("LLM API key not configured"):
        return (
            f"AI-assisted insights: {alert.get('message')}",
            "Review queue and prioritize this case based on severity and current load.",
        )

    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    explanation = f"AI-assisted insights: {lines[0]}" if lines else f"AI-assisted insights: {alert.get('message')}"
    recommendation = (
        lines[1] if len(lines) > 1 else "Review and assign to the appropriate team within the current shift."
    )
    return explanation, recommendation


async def detect_alerts() -> list[dict]:
    aggregated = aggregate_weekly_data(days=7)
    metrics = compute_metrics(aggregated)

    raw_alerts = detect_alerts_from_rules(metrics)
    ranked = rank_alerts(raw_alerts)

    enriched_alerts = []
    for alert in ranked:
        explanation, recommendation = await _explain_alert(alert)
        enriched_alerts.append(
            {
                "alert_id": f"A-{uuid4().hex[:8].upper()}",
                "type": alert["type"],
                "severity": alert["severity"],
                "priority_score": alert["priority_score"],
                "message": explanation,
                "recommendation": recommendation,
                "timestamp": alert.get("timestamp", datetime.now(timezone.utc).isoformat()),
            }
        )

    return enriched_alerts
