import json
from pathlib import Path
from threading import Lock
from app.domain.entities.risk import ClimateRisk, RiskAssessment
from app.domain.repositories.interfaces import RecommendationRepository


class JsonRecommendationRepository(RecommendationRepository):
    def __init__(self, path: Path = Path("data/recommendations.json")) -> None:
        self._path = path
        self._lock = Lock()
        self._memory: dict[str, list[RiskAssessment]] = {}

    def save(self, assessment: RiskAssessment, risk: ClimateRisk) -> None:
        with self._lock:
            self._memory.setdefault(risk.location.name, []).append(assessment)
            self._path.parent.mkdir(parents=True, exist_ok=True)
            serializable = {k: [self._flatten(a) for a in v] for k, v in self._memory.items()}
            self._path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")

    def get_by_location(self, location: str) -> list[RiskAssessment]:
        return list(self._memory.get(location, []))

    def _flatten(self, assessment: RiskAssessment) -> dict[str, object]:
        return {
            "risk_score": assessment.risk_score,
            "severity": assessment.severity,
            "priority": assessment.recommendation.priority,
            "preparedness_score": assessment.preparedness.score,
        }
