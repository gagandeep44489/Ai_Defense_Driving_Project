from dataclasses import dataclass


@dataclass(frozen=True)
class Borrower:
    """Represents a borrower profile."""

    borrower_id: str
    age: int
    annual_income: float
    credit_history_years: float
    debt_to_income: float
    employment_years: float


@dataclass(frozen=True)
class Loan:
    """Represents loan details."""

    loan_id: str
    amount: float
    interest_rate: float
    tenor_months: int
    collateral_value: float


@dataclass(frozen=True)
class RiskProfile:
    """Represents computed risk metrics."""

    pd: float
    lgd: float
    ead: float
    expected_loss: float
    credit_score: int
    risk_category: str
