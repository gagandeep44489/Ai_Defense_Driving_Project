from __future__ import annotations


def _pct(part: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((part / total) * 100, 2)


def _trend_summary(day_counts: dict[str, int]) -> dict:
    ordered = [
        ("Monday", day_counts.get("Monday", 0)),
        ("Tuesday", day_counts.get("Tuesday", 0)),
        ("Wednesday", day_counts.get("Wednesday", 0)),
        ("Thursday", day_counts.get("Thursday", 0)),
        ("Friday", day_counts.get("Friday", 0)),
        ("Saturday", day_counts.get("Saturday", 0)),
        ("Sunday", day_counts.get("Sunday", 0)),
    ]
    growth = []
    previous = None
    for day, value in ordered:
        if previous is None or previous == 0:
            growth.append({"day": day, "count": value, "wow_change_pct": 0.0})
        else:
            growth.append(
                {
                    "day": day,
                    "count": value,
                    "wow_change_pct": round(((value - previous) / previous) * 100, 2),
                }
            )
        previous = value

    return {"series": growth, "latest_week_total": sum(v for _, v in ordered)}


def compute_metrics(aggregated: dict) -> dict:
    total_patients = len(aggregated["patient_ids_seen"])
    new_patients = len(aggregated["new_patient_ids"])
    returning_patients = max(0, total_patients - new_patients)

    consultation_times = aggregated["consultation_times"]
    avg_consultation_time = round(sum(consultation_times) / len(consultation_times), 2) if consultation_times else 0.0

    risk_counts = aggregated["risk_counts"]
    total_risk_predictions = sum(risk_counts.values())

    top_risk_factors = sorted(
        aggregated["risk_factor_counts"].items(), key=lambda x: x[1], reverse=True
    )[:5]

    top_diseases = sorted(
        aggregated["disease_counts"].items(), key=lambda x: x[1], reverse=True
    )[:5]
    early_warning_signals = [
        {"symptom": k, "count": v}
        for k, v in sorted(
            aggregated["symptom_alert_counts"].items(), key=lambda x: x[1], reverse=True
        )[:3]
    ]

    doctor_workload = {}
    overloaded_doctors = 0
    underutilized_doctors = 0
    for doctor_id, scores in aggregated["doctor_workload_scores"].items():
        avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0
        level_counts = aggregated["doctor_load_levels"].get(doctor_id, {})
        overloaded = level_counts.get("overloaded", 0)
        underutilized = level_counts.get("underutilized", 0)
        if overloaded > 0:
            overloaded_doctors += 1
        if underutilized > 0:
            underutilized_doctors += 1
        doctor_workload[doctor_id] = {
            "average_workload_score": avg_score,
            "overloaded_events": overloaded,
            "underutilized_events": underutilized,
        }

    all_events = aggregated["events"]
    total_predictions = len(
        [
            e
            for e in all_events
            if e.event_type in {"risk_prediction", "workload_prediction", "disease_prediction", "anomaly_prediction"}
        ]
    )
    avg_response_time = (
        round(sum(e.response_time_ms for e in all_events) / len(all_events), 2) if all_events else 0.0
    )
    errors = len([e for e in all_events if not e.success])

    return {
        "patient_stats": {
            "total_patients": total_patients,
            "new_patients": new_patients,
            "returning_patients": returning_patients,
            "average_consultation_time_minutes": avg_consultation_time,
            "patient_growth_trend": _trend_summary(aggregated["day_patient_counts"]),
        },
        "risk_distribution": {
            "high_pct": _pct(risk_counts["High"], total_risk_predictions),
            "medium_pct": _pct(risk_counts["Medium"], total_risk_predictions),
            "low_pct": _pct(risk_counts["Low"], total_risk_predictions),
            "counts": risk_counts,
            "top_contributing_factors": top_risk_factors,
        },
        "disease_trends": {
            "most_frequent_predicted_diseases": top_diseases,
            "weekly_comparison": top_diseases,
            "early_warning_signals": early_warning_signals,
        },
        "workload_summary": {
            "average_workload_per_doctor": doctor_workload,
            "overloaded_doctors": overloaded_doctors,
            "underutilized_doctors": underutilized_doctors,
            "peak_days": aggregated["peak_by_day"],
        },
        "system_metrics": {
            "ai_predictions_made": total_predictions,
            "average_response_time_ms": avg_response_time,
            "error_rate_pct": _pct(errors, len(all_events)),
        },
    }
