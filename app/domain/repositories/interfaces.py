from abc import ABC, abstractmethod
from app.domain.entities.risk import ClimateRisk, RiskAssessment, Recommendation, RiskType


class RecommendationRepository(ABC):
    @abstractmethod
    def save(self, assessment: RiskAssessment, risk: ClimateRisk) -> None: ...

    @abstractmethod
    def get_by_location(self, location: str) -> list[RiskAssessment]: ...


class RiskRepository(ABC):
    @abstractmethod
    def save(self, risk: ClimateRisk) -> None: ...


class WeatherRepository(ABC):
    @abstractmethod
    def get_climate_trend(self, location: str, risk_type: RiskType) -> str: ...
