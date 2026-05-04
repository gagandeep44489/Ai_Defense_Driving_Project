import logging

from fastapi import FastAPI
from pydantic import BaseModel, Field

from credit_risk_simulator.application.use_cases.risk_use_cases import PredictRiskUseCase, SimulatePortfolioUseCase
from credit_risk_simulator.domain.entities.models import Borrower, Loan
from credit_risk_simulator.domain.services.credit_services import CreditScoringService, RiskAssessmentService
from credit_risk_simulator.infrastructure.config.logging_config import configure_logging
from credit_risk_simulator.infrastructure.config.settings import ConfigLoader
from credit_risk_simulator.infrastructure.data.synthetic_data import SyntheticDataSource
from credit_risk_simulator.infrastructure.models.risk_models import LogisticRegressionRiskModel
from credit_risk_simulator.infrastructure.simulation.monte_carlo import MonteCarloSimulator

configure_logging()
logger = logging.getLogger(__name__)
app = FastAPI(title="Credit Risk Simulator")


class BorrowerInput(BaseModel):
    borrower_id: str
    age: int
    annual_income: float
    credit_history_years: float
    debt_to_income: float = Field(ge=0, le=1)
    employment_years: float


class LoanInput(BaseModel):
    loan_id: str
    amount: float
    interest_rate: float
    tenor_months: int
    collateral_value: float


class RiskRequest(BaseModel):
    borrower: BorrowerInput
    loan: LoanInput
    scenario: str = "base"


config = ConfigLoader.load("config.yaml")
data_source = SyntheticDataSource()
model = LogisticRegressionRiskModel()
model.train(data_source.load_training_data(), "default")
risk_service = RiskAssessmentService(
    risk_model=model,
    scoring_service=CreditScoringService(),
    scenario_map={
        "base": config.scenarios.base,
        "recession": config.scenarios.recession,
        "growth": config.scenarios.growth,
        "inflation_shock": config.scenarios.inflation_shock,
    },
)
predict_use_case = PredictRiskUseCase(risk_service)
simulator = MonteCarloSimulator(risk_service, {"base": 0.5, "recession": 0.25, "growth": 0.2, "inflation_shock": 0.05})
simulate_use_case = SimulatePortfolioUseCase(simulator)


@app.post("/predict-risk")
def predict_risk(request: RiskRequest) -> dict:
    borrower = Borrower(**request.borrower.model_dump())
    loan = Loan(**request.loan.model_dump())
    response = predict_use_case.execute(borrower, loan, request.scenario)
    logger.info("risk prediction completed")
    return response


@app.post("/simulate-portfolio")
def simulate_portfolio(requests: list[RiskRequest]) -> dict:
    portfolio = [
        (Borrower(**item.borrower.model_dump()), Loan(**item.loan.model_dump()))
        for item in requests
    ]
    response = simulate_use_case.execute(portfolio, config.simulation_iterations)
    logger.info("portfolio simulation completed")
    return response
