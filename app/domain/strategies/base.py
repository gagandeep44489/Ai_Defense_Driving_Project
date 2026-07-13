from abc import ABC, abstractmethod
from app.domain.entities.risk import ClimateRisk, Recommendation


class RecommendationStrategy(ABC):
    @abstractmethod
    def generate(self, risk: ClimateRisk, risk_score: int) -> Recommendation: ...
