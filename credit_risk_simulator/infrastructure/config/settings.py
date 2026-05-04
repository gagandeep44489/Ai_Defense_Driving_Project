from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ScenarioConfig:
    recession: float
    growth: float
    inflation_shock: float
    base: float = 1.0


@dataclass(frozen=True)
class AppConfig:
    simulation_iterations: int
    var_percentile: float
    scenarios: ScenarioConfig


class ConfigLoader:
    """Loads configuration from YAML files."""

    @staticmethod
    def load(path: str | Path) -> AppConfig:
        with open(path, "r", encoding="utf-8") as file:
            raw: dict[str, Any] = yaml.safe_load(file)
        scenarios = ScenarioConfig(**raw["scenarios"])
        return AppConfig(
            simulation_iterations=raw["simulation_iterations"],
            var_percentile=raw["var_percentile"],
            scenarios=scenarios,
        )
