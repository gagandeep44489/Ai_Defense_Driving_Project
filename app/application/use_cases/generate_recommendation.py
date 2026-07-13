from app.application.dto.schemas import ClimateRiskRequest, RecommendationResponse
from app.domain.entities.risk import ClimateRisk, Location, RiskAssessment
from app.domain.services.engine import RecommendationEngine


class GenerateRecommendationUseCase:
    def __init__(self, engine: RecommendationEngine) -> None:
        self._engine = engine

    def execute(self, request: ClimateRiskRequest) -> RecommendationResponse:
        risk = ClimateRisk(location=Location(request.location), **request.model_dump(exclude={"location"}))
        return self._to_response(self._engine.assess(risk))

    def history(self, location: str) -> list[RecommendationResponse]:
        return [self._to_response(item) for item in self._engine.history(location)]

    def _to_response(self, assessment: RiskAssessment) -> RecommendationResponse:
        return RecommendationResponse(
            risk_score=assessment.risk_score,
            severity=assessment.severity,
            recommendations=list(assessment.recommendation.recommendations),
            priority=assessment.recommendation.priority,
            preparedness_score=assessment.preparedness.score,
            preparedness_explanation=assessment.preparedness.explanation,
            long_term_actions=list(assessment.recommendation.long_term_actions),
            categories=list(assessment.recommendation.categories),
        )
