from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_login_page():
    response = client.get("/login")

    assert response.status_code == 200