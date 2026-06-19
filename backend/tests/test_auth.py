import pytest
from fastapi.testclient import TestClient


def test_registro_exitoso(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "nombre": "Juan Pérez",
            "email": "juan@test.com",
            "password": "Segura123!",
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "juan@test.com"
    assert response.json()["role"] == "lector"
    assert response.json()["activo"] is True


def test_registro_email_duplicado(client: TestClient, usuario_lector):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "nombre": "Otro Usuario",
            "email": "lector@test.com",
            "password": "Segura123!",
        },
    )
    assert response.status_code == 409


def test_login_exitoso(client: TestClient, usuario_lector):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "lector@test.com", "password": "Lector123!"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert response.json()["role"] == "lector"


def test_login_credenciales_invalidas(client: TestClient, usuario_lector):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "lector@test.com", "password": "WrongPassword"},
    )
    assert response.status_code == 401


def test_endpoint_privado_sin_token(client: TestClient):
    response = client.get("/api/v1/prestamos/mis-prestamos")
    assert response.status_code == 403
