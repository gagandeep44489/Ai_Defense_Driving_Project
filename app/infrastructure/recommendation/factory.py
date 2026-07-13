from app.domain.entities.risk import RiskType
from app.domain.strategies.base import RecommendationStrategy
from app.domain.strategies.catalog import (
    AirPollutionRecommendationStrategy,
    CycloneRecommendationStrategy,
    DroughtRecommendationStrategy,
    FloodRecommendationStrategy,
    ForestFireRecommendationStrategy,
    HeatwaveRecommendationStrategy,
    LandslideRecommendationStrategy,
    WaterScarcityRecommendationStrategy,
)


class RecommendationStrategyFactory:
    def __init__(self) -> None:
        self._strategies: dict[RiskType, RecommendationStrategy] = {
            RiskType.FLOOD: FloodRecommendationStrategy(),
            RiskType.HEATWAVE: HeatwaveRecommendationStrategy(),
            RiskType.DROUGHT: DroughtRecommendationStrategy(),
            RiskType.AIR_POLLUTION: AirPollutionRecommendationStrategy(),
            RiskType.CYCLONE: CycloneRecommendationStrategy(),
            RiskType.LANDSLIDE: LandslideRecommendationStrategy(),
            RiskType.FOREST_FIRE: ForestFireRecommendationStrategy(),
            RiskType.WATER_SCARCITY: WaterScarcityRecommendationStrategy(),
        }

    def get(self, risk_type: RiskType) -> RecommendationStrategy:
        return self._strategies[risk_type]
