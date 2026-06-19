import pytest
from fastapi.testclient import TestClient
from app.models.libro import Libro
from app.utils.jwt import create_access_token


def test_listar_libros(client: TestClient):
    response = client.get("/api/v1/libros")
    assert response.status_code == 200
    assert "total" in response.json()
    assert "items" in response.json()


def test_crear_libro_como_admin(client: TestClient, usuario_admin):
    token = create_access_token(
        {
            "user_id": usuario_admin.id,
            "email": usuario_admin.email,
            "role": usuario_admin.role,
        }
    )

    response = client.post(
        "/api/v1/libros",
        json={
            "titulo": "Clean Code",
            "autor": "Robert C. Martin",
            "isbn": "978-0132350884",
            "categoria": "Ingeniería de Software",
            "anio_publicacion": 2008,
            "stock_total": 3,
            "descripcion": "Guía de buenas prácticas",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["titulo"] == "Clean Code"


def test_crear_libro_como_lector_falla(client: TestClient, usuario_lector):
    token = create_access_token(
        {
            "user_id": usuario_lector.id,
            "email": usuario_lector.email,
            "role": usuario_lector.role,
        }
    )

    response = client.post(
        "/api/v1/libros",
        json={
            "titulo": "Clean Code",
            "autor": "Robert C. Martin",
            "isbn": "978-0132350884",
            "categoria": "Ingeniería de Software",
            "stock_total": 3,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_obtener_libro_detalle(client: TestClient, db, usuario_admin):
    libro = Libro(
        titulo="Test Book",
        autor="Test Author",
        categoria="Test Category",
        stock_total=5,
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)

    response = client.get(f"/api/v1/libros/{libro.id}")
    assert response.status_code == 200
    assert response.json()["titulo"] == "Test Book"
    assert "disponibles" in response.json()


def test_obtener_libro_no_existente(client: TestClient):
    response = client.get("/api/v1/libros/999")
    assert response.status_code == 404
