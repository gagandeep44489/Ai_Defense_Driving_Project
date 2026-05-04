from credit_risk_simulator.domain.entities.models import Borrower, Loan
from credit_risk_simulator.domain.services.credit_services import CreditScoringService, RiskAssessmentService
from credit_risk_simulator.infrastructure.data.synthetic_data import SyntheticDataSource
from credit_risk_simulator.infrastructure.models.risk_models import LogisticRegressionRiskModel, RuleBasedRiskModel


def make_entities() -> tuple[Borrower, Loan]:
    borrower = Borrower("b1", 35, 85000, 8, 0.32, 6)
    loan = Loan("l1", 30000, 0.09, 48, 20000)
    return borrower, loan


def test_rule_model_assessment_outputs_valid_range() -> None:
    borrower, loan = make_entities()
    svc = RiskAssessmentService(RuleBasedRiskModel(), CreditScoringService(), {"base": 1.0})
    profile = svc.assess(borrower, loan)
    assert 0 < profile.pd < 1
    assert 0 <= profile.lgd <= 1
    assert profile.expected_loss > 0


def test_logistic_model_training_and_assessment() -> None:
    data = SyntheticDataSource(sample_size=300).load_training_data()
    model = LogisticRegressionRiskModel()
    model.train(data, "default")
    borrower, loan = make_entities()
    svc = RiskAssessmentService(model, CreditScoringService(), {"base": 1.0, "recession": 1.3})
    base = svc.assess(borrower, loan, "base")
    recession = svc.assess(borrower, loan, "recession")
    assert recession.pd >= base.pd
