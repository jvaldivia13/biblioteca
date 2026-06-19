import pytest
from fastapi.testclient import TestClient
from app.utils.jwt import create_access_token


def test_obtener_estadisticas(client: TestClient, usuario_admin):
    token = create_access_token(
        {
            "user_id": usuario_admin.id,
            "email": usuario_admin.email,
            "role": usuario_admin.role,
        }
    )

    response = client.get(
        "/api/v1/admin/stats",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "total_libros" in response.json()
    assert "total_usuarios" in response.json()
    assert "prestamos_activos" in response.json()


def test_listar_usuarios(client: TestClient, usuario_admin):
    token = create_access_token(
        {
            "user_id": usuario_admin.id,
            "email": usuario_admin.email,
            "role": usuario_admin.role,
        }
    )

    response = client.get(
        "/api/v1/admin/usuarios",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "total" in response.json()
    assert "items" in response.json()


def test_no_admin_rechaza_admin_endpoint(client: TestClient, usuario_lector):
    token = create_access_token(
        {
            "user_id": usuario_lector.id,
            "email": usuario_lector.email,
            "role": usuario_lector.role,
        }
    )

    response = client.get(
        "/api/v1/admin/stats",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
