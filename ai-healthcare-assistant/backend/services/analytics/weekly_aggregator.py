from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone

from services.analytics.event_store import EventRecord, analytics_store


def _default_weekday_map() -> dict[str, int]:
    return {
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 0,
    }


def aggregate_weekly_data(days: int = 7) -> dict:
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=days)
    events = analytics_store.get_events_since(since)

    patient_ids_seen: set[str] = set()
    first_visit_seen: set[str] = set()
    consultation_times: list[float] = []
    day_patient_counts = _default_weekday_map()
    risk_counts = {"Low": 0, "Medium": 0, "High": 0}
    risk_factor_counts: dict[str, int] = defaultdict(int)
    disease_counts: dict[str, int] = defaultdict(int)
    symptom_alert_counts: dict[str, int] = defaultdict(int)
    doctor_workload_scores: dict[str, list[float]] = defaultdict(list)
    doctor_load_levels: dict[str, dict[str, int]] = defaultdict(
        lambda: {"overloaded": 0, "underutilized": 0}
    )
    peak_by_day = _default_weekday_map()

    for event in events:
        weekday = event.timestamp.strftime("%A")

        if event.event_type == "patient_visit":
            patient_id = event.payload.get("patient_id", "unknown")
            patient_ids_seen.add(patient_id)
            if event.payload.get("is_new_patient", False):
                first_visit_seen.add(patient_id)

            consultation_time = float(event.payload.get("consultation_time_minutes", 0))
            if consultation_time > 0:
                consultation_times.append(consultation_time)

            day_patient_counts[weekday] += 1
            hour_bucket = event.payload.get("hour_bucket", "unknown")
            if hour_bucket != "unknown":
                peak_by_day[weekday] += 1

            for symptom in event.payload.get("symptoms", []):
                symptom_alert_counts[symptom] += 1

        elif event.event_type == "risk_prediction":
            level = event.payload.get("risk_level", "Medium")
            if level in risk_counts:
                risk_counts[level] += 1
            for factor in event.payload.get("factors", []):
                risk_factor_counts[factor] += 1

        elif event.event_type == "disease_prediction":
            for disease in event.payload.get("diseases", []):
                disease_counts[disease] += 1

        elif event.event_type == "workload_prediction":
            doctor_id = event.payload.get("doctor_id", "doctor-unassigned")
            score = float(event.payload.get("workload_score", 0))
            doctor_workload_scores[doctor_id].append(score)
            level = event.payload.get("workload_level", "Low")
            if level == "High":
                doctor_load_levels[doctor_id]["overloaded"] += 1
            if level == "Low":
                doctor_load_levels[doctor_id]["underutilized"] += 1

    return {
        "window_days": days,
        "total_events": len(events),
        "events": events,
        "patient_ids_seen": patient_ids_seen,
        "new_patient_ids": first_visit_seen,
        "consultation_times": consultation_times,
        "day_patient_counts": day_patient_counts,
        "risk_counts": risk_counts,
        "risk_factor_counts": dict(risk_factor_counts),
        "disease_counts": dict(disease_counts),
        "symptom_alert_counts": dict(symptom_alert_counts),
        "doctor_workload_scores": dict(doctor_workload_scores),
        "doctor_load_levels": dict(doctor_load_levels),
        "peak_by_day": peak_by_day,
    }
