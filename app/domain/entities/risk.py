from dataclasses import dataclass, field
from enum import StrEnum


class RiskType(StrEnum):
    FLOOD = "Flood"
    HEATWAVE = "Heatwave"
    DROUGHT = "Drought"
    AIR_POLLUTION = "Air Pollution"
    CYCLONE = "Cyclone"
    LANDSLIDE = "Landslide"
    FOREST_FIRE = "Forest Fire"
    WATER_SCARCITY = "Water Scarcity"


class RiskLevel(StrEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass(frozen=True, slots=True)
class Location:
    name: str
    region: str | None = None


@dataclass(frozen=True, slots=True)
class ClimateRisk:
    location: Location
    risk_type: RiskType
    risk_level: RiskLevel
    rainfall_mm: float | None = None
    river_level: float | None = None
    temperature_c: float | None = None
    air_quality_index: int | None = None
    wind_speed_kph: float | None = None
    population: int = 0
    infrastructure: str = "Moderate"
    historical_events: int = 0
    climate_trend: str = "Stable"
    vulnerable_population: int = 0
    critical_facilities: int = 0


@dataclass(frozen=True, slots=True)
class PreparednessScore:
    score: int
    explanation: str
    factors: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Recommendation:
    recommendations: tuple[str, ...]
    priority: str
    long_term_actions: tuple[str, ...]
    categories: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RiskAssessment:
    risk_score: int
    severity: str
    recommendation: Recommendation
    preparedness: PreparednessScore
