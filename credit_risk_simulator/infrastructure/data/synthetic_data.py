from dataclasses import dataclass

import numpy as np
import pandas as pd

from credit_risk_simulator.domain.interfaces.contracts import DataSourceInterface


@dataclass
class SyntheticDataSource(DataSourceInterface):
    sample_size: int = 1500
    random_state: int = 42

    def load_training_data(self) -> pd.DataFrame:
        rng = np.random.default_rng(self.random_state)
        age = rng.integers(21, 70, self.sample_size)
        income = rng.normal(80000, 25000, self.sample_size).clip(18000, 250000)
        history = rng.uniform(0.5, 25.0, self.sample_size)
        dti = rng.uniform(0.05, 0.85, self.sample_size)
        employment = rng.uniform(0.0, 30.0, self.sample_size)
        loan_amount = rng.normal(35000, 20000, self.sample_size).clip(2000, 180000)
        collateral = (loan_amount * rng.uniform(0.3, 1.5, self.sample_size)).clip(500, 250000)
        rate = rng.uniform(0.02, 0.25, self.sample_size)

        risk_signal = (
            2.6 * dti
            - 0.000008 * income
            + 0.00002 * loan_amount
            - 0.05 * history
            - 0.03 * employment
            + 0.2 * (rate > 0.18)
        )
        probs = 1 / (1 + np.exp(-risk_signal))
        default = rng.binomial(1, probs)

        return pd.DataFrame(
            {
                "age": age,
                "annual_income": income,
                "credit_history_years": history,
                "debt_to_income": dti,
                "employment_years": employment,
                "loan_amount": loan_amount,
                "collateral_value": collateral,
                "interest_rate": rate,
                "default": default,
            }
        )
