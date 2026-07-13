from app.domain.entities.risk import ClimateRisk, RiskAssessment
from app.domain.repositories.interfaces import RecommendationRepository
from app.domain.services.preparedness import PreparednessScoringService
from app.infrastructure.recommendation.factory import RecommendationStrategyFactory


class RecommendationEngine:
    def __init__(
        self,
        repository: RecommendationRepository,
        strategy_factory: RecommendationStrategyFactory,
        preparedness_service: PreparednessScoringService,
    ) -> None:
        self._repository = repository
        self._strategy_factory = strategy_factory
        self._preparedness_service = preparedness_service

    def assess(self, risk: ClimateRisk) -> RiskAssessment:
        preparedness = self._preparedness_service.calculate(risk)
        risk_score = self._risk_score(risk, preparedness.score)
        strategy = self._strategy_factory.get(risk.risk_type)
        recommendation = strategy.generate(risk, risk_score)
        assessment = RiskAssessment(risk_score, self._severity(risk_score), recommendation, preparedness)
        self._repository.save(assessment, risk)
        return assessment

    def history(self, location: str) -> list[RiskAssessment]:
        return self._repository.get_by_location(location)

    def _risk_score(self, risk: ClimateRisk, preparedness: int) -> int:
        level = {"Low": 25, "Medium": 50, "High": 75, "Critical": 90}[risk.risk_level.value]
        exposure = min(12, risk.population / 2500) + min(10, risk.historical_events * 2)
        vulnerability = min(10, risk.vulnerable_population / 1000) + risk.critical_facilities * 2
        climate = 5 if risk.climate_trend.lower() in {"worsening", "increasing"} else 0
        score = level + exposure + vulnerability + climate - ((preparedness - 50) * 0.35)
        return max(0, min(100, round(score)))

    def _severity(self, score: int) -> str:
        if score >= 85:
            return "Critical"
        if score >= 70:
            return "High"
        if score >= 45:
            return "Medium"
        return "Low"
