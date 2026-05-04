from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression

from credit_risk_simulator.domain.entities.models import Borrower, Loan
from credit_risk_simulator.domain.interfaces.contracts import RiskModelInterface


FEATURES = [
    "age",
    "annual_income",
    "credit_history_years",
    "debt_to_income",
    "employment_years",
    "loan_amount",
    "collateral_value",
    "interest_rate",
]


@dataclass
class LogisticRegressionRiskModel(RiskModelInterface):
    random_state: int = 42
    _model: LogisticRegression = field(default_factory=lambda: LogisticRegression(max_iter=1000))
    _is_trained: bool = False

    def train(self, data: pd.DataFrame, target_column: str) -> None:
        x = data[FEATURES]
        y = data[target_column]
        sampler = SMOTE(random_state=self.random_state)
        x_resampled, y_resampled = sampler.fit_resample(x, y)
        self._model.fit(x_resampled, y_resampled)
        self._is_trained = True

    def predict_pd(self, borrower: Borrower, loan: Loan, scenario_factor: float = 1.0) -> float:
        if not self._is_trained:
            raise RuntimeError("Model must be trained before prediction")

        row = np.array(
            [[
                borrower.age,
                borrower.annual_income,
                borrower.credit_history_years,
                borrower.debt_to_income,
                borrower.employment_years,
                loan.amount,
                loan.collateral_value,
                loan.interest_rate,
            ]]
        )
        pd_value = float(self._model.predict_proba(row)[0][1])
        return min(max(pd_value * scenario_factor, 0.0001), 0.999)


@dataclass
class RuleBasedRiskModel(RiskModelInterface):
    """Simple scorecard-style rule model."""

    def train(self, data: pd.DataFrame, target_column: str) -> None:  # noqa: ARG002
        return None

    def predict_pd(self, borrower: Borrower, loan: Loan, scenario_factor: float = 1.0) -> float:
        score = 0.02
        if borrower.debt_to_income > 0.5:
            score += 0.15
        if borrower.credit_history_years < 2:
            score += 0.1
        if borrower.annual_income < 35000:
            score += 0.1
        if loan.amount > borrower.annual_income * 0.8:
            score += 0.12
        if borrower.employment_years < 1:
            score += 0.07
        return min(max(score * scenario_factor, 0.0001), 0.999)
