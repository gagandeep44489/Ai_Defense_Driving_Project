from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health() -> None:
    r = client.get('/api/v1/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_predict_risk() -> None:
    payload = {
        "supplier": {
            "country": "US",
            "cost": 600,
            "delivery_time": 16,
            "reliability_score": 75,
            "defect_rate": 0.11,
            "delay_history": 6,
        },
        "headlines": ["Factory delay reported in region"],
    }
    r = client.post('/api/v1/predict-risk', json=payload)
    assert r.status_code in (200, 503)
    if r.status_code == 200:
        body = r.json()
        assert body["risk_level"] in ["Low", "Medium", "High"]
        assert 0 <= body["confidence"] <= 1
