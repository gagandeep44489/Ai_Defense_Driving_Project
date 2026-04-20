from __future__ import annotations


def calculate_priority(alert: dict) -> float:
    priority_score = (
        (float(alert.get("risk_score", 0)) * 0.4)
        + (float(alert.get("trend_spike", 0)) * 0.3)
        + (float(alert.get("workload_score", 0)) * 0.2 / 100)
        + (float(alert.get("system_health", 0)) * 0.1)
    )
    return round(priority_score, 2)


def severity_from_priority(priority_score: float) -> str:
    if priority_score >= 6:
        return "Critical"
    if priority_score >= 4:
        return "High"
    if priority_score >= 2:
        return "Medium"
    return "Low"


def rank_alerts(alerts: list[dict]) -> list[dict]:
    for alert in alerts:
        score = calculate_priority(alert)
        alert["priority_score"] = score
        alert["severity"] = severity_from_priority(score)
    return sorted(alerts, key=lambda x: x["priority_score"], reverse=True)
