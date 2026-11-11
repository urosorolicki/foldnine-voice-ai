from fastapi.testclient import TestClient
from app.main import app


def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_empty_message_rejected():
    response = TestClient(app).post("/api/chat", json={"message": ""})
    assert response.status_code == 422
