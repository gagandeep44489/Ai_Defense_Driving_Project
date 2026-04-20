from __future__ import annotations

from datetime import datetime, timedelta, timezone

from services.analytics.event_store import EventRecord, analytics_store


def _recent_events(hours: int = 24) -> list[EventRecord]:
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    return analytics_store.get_events_since(since)


def _system_health_score(events: list[EventRecord]) -> float:
    if not events:
        return 0.0
    error_rate = len([e for e in events if not e.success]) / len(events)
    avg_latency = sum(e.response_time_ms for e in events) / len(events)

    error_component = min(error_rate * 10, 10)
    latency_component = min(avg_latency / 200, 10)
    return round((error_component + latency_component) / 2, 2)


def detect_patient_risk_alerts(events: list[EventRecord], risk_threshold: int = 7) -> list[dict]:
    alerts: list[dict] = []
    for event in events:
        if event.event_type != "risk_prediction" or not event.success:
            continue
        risk_score = float(event.payload.get("score", 0))
        if risk_score >= risk_threshold:
            alerts.append(
                {
                    "type": "Patient Risk",
                    "message": "High-risk patient detected with elevated symptom complexity.",
                    "risk_score": risk_score,
                    "trend_spike": 0,
                    "workload_score": 0,
                    "system_health": 0,
                    "timestamp": event.timestamp.isoformat(),
                }
            )
    return alerts


def detect_disease_trend_alerts(metrics: dict) -> list[dict]:
    alerts: list[dict] = []
    warning_signals = metrics.get("disease_trends", {}).get("early_warning_signals", [])
    if not warning_signals:
        return alerts

    top_signal = warning_signals[0]
    spike = float(top_signal.get("count", 0))
    if spike >= 3:
        alerts.append(
            {
                "type": "Disease Trend",
                "message": f"Spike in {top_signal.get('symptom', 'respiratory')} related cases this week.",
                "risk_score": 0,
                "trend_spike": spike,
                "workload_score": 0,
                "system_health": 0,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
    return alerts


def detect_workload_alerts(events: list[EventRecord], workload_threshold: float = 420) -> list[dict]:
    alerts: list[dict] = []
    for event in events:
        if event.event_type != "workload_prediction" or not event.success:
            continue
        workload_score = float(event.payload.get("workload_score", 0))
        if workload_score >= workload_threshold:
            alerts.append(
                {
                    "type": "Doctor Workload",
                    "message": "Doctor workload is high with complex case mix.",
                    "risk_score": 0,
                    "trend_spike": 0,
                    "workload_score": workload_score,
                    "system_health": 0,
                    "timestamp": event.timestamp.isoformat(),
                }
            )
    return alerts


def detect_system_alerts(events: list[EventRecord]) -> list[dict]:
    alerts: list[dict] = []
    if not events:
        return alerts

    failed_events = [e for e in events if not e.success]
    avg_latency = sum(e.response_time_ms for e in events) / len(events)
    health_score = _system_health_score(events)

    if avg_latency > 800:
        alerts.append(
            {
                "type": "System",
                "message": "API latency is above target and may delay care operations.",
                "risk_score": 0,
                "trend_spike": 0,
                "workload_score": 0,
                "system_health": health_score,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    if failed_events:
        alerts.append(
            {
                "type": "System",
                "message": "Model/API failures detected in recent operations.",
                "risk_score": 0,
                "trend_spike": 0,
                "workload_score": 0,
                "system_health": max(health_score, 6),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    return alerts


def detect_alerts_from_rules(metrics: dict) -> list[dict]:
    events = _recent_events(hours=24)

    alerts: list[dict] = []
    alerts.extend(detect_patient_risk_alerts(events))
    alerts.extend(detect_disease_trend_alerts(metrics))
    alerts.extend(detect_workload_alerts(events))
    alerts.extend(detect_system_alerts(events))
    return alerts
