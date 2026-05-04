from fastapi.testclient import TestClient

from credit_risk_simulator.presentation.api import app


def test_predict_risk_endpoint() -> None:
    client = TestClient(app)
    payload = {
        "borrower": {
            "borrower_id": "b1",
            "age": 30,
            "annual_income": 70000,
            "credit_history_years": 5,
            "debt_to_income": 0.4,
            "employment_years": 3,
        },
        "loan": {
            "loan_id": "l1",
            "amount": 25000,
            "interest_rate": 0.11,
            "tenor_months": 36,
            "collateral_value": 12000,
        },
        "scenario": "base",
    }
    response = client.post("/predict-risk", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "expected_loss" in body
