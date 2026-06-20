import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta
from app.models.libro import Libro
from app.models.prestamo import Prestamo
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


def auth_header(usuario):
    token = create_access_token(
        {"user_id": usuario.id, "email": usuario.email, "role": usuario.role}
    )
    return {"Authorization": f"Bearer {token}"}


def crear_libro(db, stock_total=1):
    libro = Libro(
        titulo="Libro Retorno",
        autor="Autora",
        categoria="Pruebas",
        stock_total=stock_total,
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


def crear_prestamo(db, usuario, libro):
    prestamo = Prestamo(
        usuario_id=usuario.id,
        libro_id=libro.id,
        fecha_prestamo=date.today(),
        fecha_devolucion_esperada=date.today() + timedelta(days=14),
        estado="activo",
    )
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo


def test_admin_puede_devolver_prestamo_de_otro_usuario(
    client: TestClient, db, usuario_admin, usuario_lector
):
    libro = crear_libro(db)
    prestamo = crear_prestamo(db, usuario_lector, libro)

    response = client.put(
        f"/api/v1/prestamos/{prestamo.id}/devolver",
        headers=auth_header(usuario_admin),
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "devuelto"


def test_lector_no_puede_devolver_prestamo_de_otro_usuario(
    client: TestClient, db, usuario_lector
):
    from app.models.usuario import Usuario
    from app.utils.password import hash_password

    otro_lector = Usuario(
        nombre="Otro Lector",
        email="otro-lector@test.com",
        password_hash=hash_password("Lector123!"),
        role="lector",
        activo=True,
    )
    db.add(otro_lector)
    db.commit()
    db.refresh(otro_lector)

    libro = crear_libro(db)
    prestamo = crear_prestamo(db, otro_lector, libro)

    response = client.put(
        f"/api/v1/prestamos/{prestamo.id}/devolver",
        headers=auth_header(usuario_lector),
    )

    assert response.status_code == 403


def test_devolucion_incrementa_disponibilidad(client: TestClient, db, usuario_lector):
    libro = crear_libro(db, stock_total=1)
    prestamo = crear_prestamo(db, usuario_lector, libro)

    before = client.get(f"/api/v1/libros/{libro.id}").json()
    assert before["disponibles"] == 0

    response = client.put(
        f"/api/v1/prestamos/{prestamo.id}/devolver",
        headers=auth_header(usuario_lector),
    )
    assert response.status_code == 200

    after = client.get(f"/api/v1/libros/{libro.id}").json()
    assert after["disponibles"] == 1
