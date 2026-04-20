from __future__ import annotations


def _complexity_factor(complexity_score: float) -> float:
    if complexity_score >= 6:
        return 1.5
    if complexity_score >= 3:
        return 1.2
    return 1.0


def _score_to_workload(score: float) -> str:
    if score >= 480:
        return "High"
    if score >= 240:
        return "Medium"
    return "Low"


def _suggestions(workload_level: str) -> list[str]:
    if workload_level == "High":
        return [
            "Reschedule non-critical patients",
            "Allocate assistant support",
            "Split complex cases across specialist slots",
        ]
    if workload_level == "Medium":
        return [
            "Reserve overflow slots for medium/high-risk patients",
            "Allocate assistant support",
        ]
    return [
        "Maintain current schedule",
        "Use open slots for preventive follow-ups",
    ]


def predict_workload(payload: dict) -> dict:
    patients_per_day: int = payload.get("patients_per_day", 0)
    average_consultation_minutes: float = payload.get("average_consultation_minutes", 0)
    complexity_score: float = payload.get("complexity_score", 0)

    factor = _complexity_factor(complexity_score)
    workload_score = patients_per_day * average_consultation_minutes * factor
    workload_level = _score_to_workload(workload_score)

    return {
        "workload_level": workload_level,
        "workload_score": round(workload_score, 2),
        "complexity_factor": factor,
        "suggested_actions": _suggestions(workload_level),
        "label": "AI-assisted insights",
    }
