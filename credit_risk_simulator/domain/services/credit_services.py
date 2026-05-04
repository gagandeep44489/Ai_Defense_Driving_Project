from dataclasses import dataclass

from credit_risk_simulator.domain.entities.models import Borrower, Loan, RiskProfile
from credit_risk_simulator.domain.interfaces.contracts import RiskAssessmentInterface, RiskModelInterface


@dataclass
class CreditScoringService:
    """Converts risk factors into a 300-900 credit score."""

    def score(self, pd: float, lgd: float, dti: float) -> int:
        base = 900
        penalty = (pd * 400) + (lgd * 150) + (dti * 120)
        return int(min(max(base - penalty, 300), 900))


@dataclass
class RiskAssessmentService(RiskAssessmentInterface):
    """Computes PD, LGD, EAD and expected loss."""

    risk_model: RiskModelInterface
    scoring_service: CreditScoringService
    scenario_map: dict[str, float]

    def assess(self, borrower: Borrower, loan: Loan, scenario: str = "base") -> RiskProfile:
        factor = self.scenario_map.get(scenario, 1.0)
        pd_value = self.risk_model.predict_pd(borrower, loan, factor)
        ead = loan.amount
        recovery_rate = min(loan.collateral_value / max(loan.amount, 1.0), 1.0)
        lgd = max(0.05, 1.0 - recovery_rate)
        expected_loss = pd_value * lgd * ead
        score = self.scoring_service.score(pd_value, lgd, borrower.debt_to_income)
        category = "Low" if score >= 700 else "Medium" if score >= 580 else "High"
        return RiskProfile(pd_value, lgd, ead, expected_loss, score, category)
