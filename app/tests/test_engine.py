from app.domain.entities.risk import ClimateRisk, Location, RiskLevel, RiskType
from app.domain.services.engine import RecommendationEngine
from app.domain.services.preparedness import PreparednessScoringService
from app.infrastructure.recommendation.factory import RecommendationStrategyFactory
from app.infrastructure.repositories.json_repository import JsonRecommendationRepository


def test_flood_example_generates_critical_recommendation(tmp_path):
    repo = JsonRecommendationRepository(tmp_path / "recommendations.json")
    engine = RecommendationEngine(repo, RecommendationStrategyFactory(), PreparednessScoringService())
    risk = ClimateRisk(Location("Village A"), RiskType.FLOOD, RiskLevel.HIGH, rainfall_mm=285, river_level=9.8, population=15000, infrastructure="Moderate", historical_events=6)

    assessment = engine.assess(risk)

    assert assessment.risk_score >= 85
    assert assessment.severity == "Critical"
    assert "Clean drainage channels immediately" in assessment.recommendation.recommendations
    assert assessment.preparedness.score == 62


def test_all_risk_strategies_are_registered(tmp_path):
    engine = RecommendationEngine(JsonRecommendationRepository(tmp_path / "r.json"), RecommendationStrategyFactory(), PreparednessScoringService())
    for risk_type in RiskType:
        risk = ClimateRisk(Location("Test"), risk_type, RiskLevel.MEDIUM, population=1000)
        assessment = engine.assess(risk)
        assert assessment.recommendation.recommendations
