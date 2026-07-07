"""API smoke tests."""
from fastapi.testclient import TestClient
from sovereignai.api.main import create_app

def test_health() -> None:
    client = TestClient(create_app())
    assert client.get('/health').json()['status'] == 'ok'

def test_predict_bruteforce() -> None:
    client = TestClient(create_app())
    payload={'source_ip':'10.0.0.1','destination_ip':'10.0.0.2','source_port':44444,'destination_port':22,'protocol':'TCP','bytes_sent':1000,'bytes_received':100,'duration_seconds':2,'failed_logins':8}
    body = client.post('/api/v1/threats/predict', json=payload).json()
    assert body['threat_class'] == 'brute_force'
    assert body['risk_score'] >= 50
