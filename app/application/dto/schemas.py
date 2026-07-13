from pydantic import BaseModel, ConfigDict, Field
from app.domain.entities.risk import RiskLevel, RiskType


class ClimateRiskRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    location: str = Field(min_length=1, max_length=120)
    risk_type: RiskType
    risk_level: RiskLevel
    rainfall_mm: float | None = Field(default=None, ge=0)
    river_level: float | None = Field(default=None, ge=0)
    temperature_c: float | None = None
    air_quality_index: int | None = Field(default=None, ge=0, le=500)
    wind_speed_kph: float | None = Field(default=None, ge=0)
    population: int = Field(ge=0)
    infrastructure: str = Field(default="Moderate", pattern="^(Weak|Moderate|Strong)$")
    historical_events: int = Field(default=0, ge=0)
    climate_trend: str = "Stable"
    vulnerable_population: int = Field(default=0, ge=0)
    critical_facilities: int = Field(default=0, ge=0)


class RecommendationResponse(BaseModel):
    risk_score: int
    severity: str
    recommendations: list[str]
    priority: str
    preparedness_score: int
    preparedness_explanation: str
    long_term_actions: list[str]
    categories: list[str]
