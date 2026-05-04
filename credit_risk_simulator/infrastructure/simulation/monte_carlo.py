from dataclasses import dataclass
from typing import Iterable

import numpy as np

from credit_risk_simulator.domain.entities.models import Borrower, Loan
from credit_risk_simulator.domain.interfaces.contracts import SimulationEngineInterface
from credit_risk_simulator.domain.services.credit_services import RiskAssessmentService


@dataclass
class MonteCarloSimulator(SimulationEngineInterface):
    risk_service: RiskAssessmentService
    scenario_weights: dict[str, float]
    random_state: int = 42

    def run(self, portfolios: Iterable[tuple[Borrower, Loan]], iterations: int) -> dict:
        rng = np.random.default_rng(self.random_state)
        scenarios = list(self.scenario_weights.keys())
        probs = np.array(list(self.scenario_weights.values()), dtype=float)
        probs = probs / probs.sum()
        portfolio = list(portfolios)

        losses: list[float] = []
        for _ in range(iterations):
            sampled = rng.choice(scenarios, p=probs)
            total = 0.0
            for borrower, loan in portfolio:
                total += self.risk_service.assess(borrower, loan, sampled).expected_loss
            losses.append(total)

        arr = np.array(losses)
        return {
            "mean_expected_loss": float(arr.mean()),
            "loss_std": float(arr.std()),
            "var_95": float(np.percentile(arr, 95)),
            "iterations": iterations,
        }
