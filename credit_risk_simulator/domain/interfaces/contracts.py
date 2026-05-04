from abc import ABC, abstractmethod
from typing import Iterable

import pandas as pd

from credit_risk_simulator.domain.entities.models import Borrower, Loan, RiskProfile


class RiskModelInterface(ABC):
    """Contract for risk model implementations."""

    @abstractmethod
    def train(self, data: pd.DataFrame, target_column: str) -> None:
        ...

    @abstractmethod
    def predict_pd(self, borrower: Borrower, loan: Loan, scenario_factor: float = 1.0) -> float:
        ...


class DataSourceInterface(ABC):
    """Contract for data source implementations."""

    @abstractmethod
    def load_training_data(self) -> pd.DataFrame:
        ...


class SimulationEngineInterface(ABC):
    """Contract for simulation engine implementations."""

    @abstractmethod
    def run(self, portfolios: Iterable[tuple[Borrower, Loan]], iterations: int) -> dict:
        ...


class RiskAssessmentInterface(ABC):
    """Contract for risk assessment service."""

    @abstractmethod
    def assess(self, borrower: Borrower, loan: Loan, scenario: str = "base") -> RiskProfile:
        ...
