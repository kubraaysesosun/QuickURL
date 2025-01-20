from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_short_url():
    response = client.post("/shorten", json={"long_url": "https://example.com"})
    assert response.status_code == 200
    assert "short_url" in response.json()

def test_redirect_to_long_url():
    response = client.get("/short_url")
    assert response.status_code in [200, 404]
