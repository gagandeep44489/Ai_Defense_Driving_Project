from fastapi.testclient import TestClient
from app.main import app


def test_recommendations_endpoint():
    client = TestClient(app)
    response = client.post("/recommendations", json={"location":"Village A","risk_type":"Flood","risk_level":"High","rainfall_mm":285,"river_level":9.8,"population":15000,"infrastructure":"Moderate","historical_events":6})
    assert response.status_code == 200
    body = response.json()
    assert body["severity"] == "Critical"
    assert body["priority"] == "Immediate"


def test_health_endpoint():
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
