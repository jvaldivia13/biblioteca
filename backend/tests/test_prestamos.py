import pytest
from fastapi.testclient import TestClient
from app.models.libro import Libro
from app.utils.jwt import create_access_token


def test_solicitar_prestamo(client: TestClient, db, usuario_lector):
    libro = Libro(
        titulo="Test Book",
        autor="Test Author",
        categoria="Test Category",
        stock_total=5,
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)

    token = create_access_token(
        {
            "user_id": usuario_lector.id,
            "email": usuario_lector.email,
            "role": usuario_lector.role,
        }
    )

    response = client.post(
        "/api/v1/prestamos",
        json={"libro_id": libro.id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["estado"] == "activo"
    assert response.json()["vencido"] is False


def test_solicitar_prestamo_sin_stock(client: TestClient, db, usuario_lector):
    libro = Libro(
        titulo="No Stock Book",
        autor="Test Author",
        categoria="Test Category",
        stock_total=0,
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)

    token = create_access_token(
        {
            "user_id": usuario_lector.id,
            "email": usuario_lector.email,
            "role": usuario_lector.role,
        }
    )

    response = client.post(
        "/api/v1/prestamos",
        json={"libro_id": libro.id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409


def test_obtener_mis_prestamos(client: TestClient, usuario_lector):
    token = create_access_token(
        {
            "user_id": usuario_lector.id,
            "email": usuario_lector.email,
            "role": usuario_lector.role,
        }
    )

    response = client.get(
        "/api/v1/prestamos/mis-prestamos",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "total" in response.json()
    assert "items" in response.json()
