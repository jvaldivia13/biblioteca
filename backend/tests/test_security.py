from fastapi.testclient import TestClient


def test_security_headers_present(client: TestClient):
    response = client.get("/")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
