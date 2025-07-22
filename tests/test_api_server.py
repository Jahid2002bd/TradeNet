from fastapi.testclient import TestClient
from src.utils.api_server import app

def test_health_endpoint_returns_ok():
    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
