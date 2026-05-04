from dataclasses import dataclass

from credit_risk_simulator.domain.entities.models import Borrower, Loan
from credit_risk_simulator.domain.services.credit_services import RiskAssessmentService
from credit_risk_simulator.infrastructure.simulation.monte_carlo import MonteCarloSimulator


@dataclass
class PredictRiskUseCase:
    risk_service: RiskAssessmentService

    def execute(self, borrower: Borrower, loan: Loan, scenario: str) -> dict:
        profile = self.risk_service.assess(borrower, loan, scenario)
        return profile.__dict__


@dataclass
class SimulatePortfolioUseCase:
    simulator: MonteCarloSimulator

    def execute(self, portfolios: list[tuple[Borrower, Loan]], iterations: int) -> dict:
        return self.simulator.run(portfolios, iterations)
