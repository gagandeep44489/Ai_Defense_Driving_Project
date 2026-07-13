from functools import lru_cache
from app.application.use_cases.generate_recommendation import GenerateRecommendationUseCase
from app.domain.services.engine import RecommendationEngine
from app.domain.services.preparedness import PreparednessScoringService
from app.infrastructure.recommendation.factory import RecommendationStrategyFactory
from app.infrastructure.repositories.json_repository import JsonRecommendationRepository


@lru_cache
def get_use_case() -> GenerateRecommendationUseCase:
    repository = JsonRecommendationRepository()
    engine = RecommendationEngine(repository, RecommendationStrategyFactory(), PreparednessScoringService())
    return GenerateRecommendationUseCase(engine)
