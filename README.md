# Credit Risk Simulator

A production-style Python system for borrower credit risk assessment and portfolio simulation using clean architecture, SOLID principles, rule-based scoring, and ML risk prediction.

## Architecture

```text
credit_risk_simulator/
├── presentation/
│   └── api.py                    # FastAPI endpoints
├── application/
│   └── use_cases/
│       └── risk_use_cases.py     # Orchestration layer
├── domain/
│   ├── entities/
│   │   └── models.py             # Borrower, Loan, RiskProfile
│   ├── interfaces/
│   │   └── contracts.py          # Abstractions
│   └── services/
│       └── credit_services.py    # Business logic
└── infrastructure/
    ├── config/settings.py        # YAML config loader
    ├── data/synthetic_data.py    # Synthetic dataset generator
    ├── models/risk_models.py     # Logistic + rule models
    └── simulation/monte_carlo.py # Portfolio Monte Carlo engine
```

## SOLID Application

- **Single Responsibility**: each class handles one concern (e.g., `RiskAssessmentService` computes risk metrics only).
- **Open/Closed**: new risk models can be added by implementing `RiskModelInterface`.
- **Liskov Substitution**: `RuleBasedRiskModel` and `LogisticRegressionRiskModel` can be swapped interchangeably.
- **Interface Segregation**: distinct interfaces for model, data source, simulation, and assessment.
- **Dependency Inversion**: use cases and services depend on interfaces/abstractions.

## Risk Methodology

- PD estimated with model (`LogisticRegression` + `SMOTE`) or rule engine.
- LGD derived from collateral recovery: `LGD = max(0.05, 1 - collateral/loan_amount)`.
- EAD approximated as current loan amount.
- Expected Loss: `EL = PD * LGD * EAD`.
- Credit score range: **300–900** and mapped to Low/Medium/High risk.

## API Endpoints

- `POST /predict-risk`
- `POST /simulate-portfolio`

### Example `/predict-risk` request

```json
{
  "borrower": {
    "borrower_id": "b-001",
    "age": 32,
    "annual_income": 85000,
    "credit_history_years": 6,
    "debt_to_income": 0.35,
    "employment_years": 4
  },
  "loan": {
    "loan_id": "l-001",
    "amount": 30000,
    "interest_rate": 0.1,
    "tenor_months": 48,
    "collateral_value": 18000
  },
  "scenario": "recession"
}
```

## Running

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
uvicorn credit_risk_simulator.presentation.api:app --reload
pytest
```

## Config-Driven Pipeline

`config.yaml` controls scenario multipliers, simulation iterations, and VaR percentile.

## Docker

```bash
docker build -t credit-risk-simulator .
docker run -p 8000:8000 credit-risk-simulator
```

## Optional Extensions

- Add SHAP explainability on top of trained ML model.
- Build Streamlit dashboard for interactive scenario testing.
- Add asynchronous scoring for real-time inference pipelines.
