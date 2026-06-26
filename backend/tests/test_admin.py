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


def test_lector_no_puede_listar_usuarios(client: TestClient, usuario_lector):
    response = client.get(
        "/api/v1/admin/usuarios",
        headers=auth_header(usuario_lector),
    )
    assert response.status_code == 403


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


def auth_header(usuario):
    token = create_access_token(
        {"user_id": usuario.id, "email": usuario.email, "role": usuario.role}
    )
    return {"Authorization": f"Bearer {token}"}


def test_admin_rechaza_rol_invalido(client: TestClient, usuario_admin, usuario_lector):
    response = client.put(
        f"/api/v1/admin/usuarios/{usuario_lector.id}/rol",
        json={"role": "superadmin"},
        headers=auth_header(usuario_admin),
    )
    assert response.status_code == 422


def test_admin_no_puede_quitarse_su_propio_rol(client: TestClient, usuario_admin):
    response = client.put(
        f"/api/v1/admin/usuarios/{usuario_admin.id}/rol",
        json={"role": "lector"},
        headers=auth_header(usuario_admin),
    )
    assert response.status_code == 409


def test_admin_puede_cambiar_rol_de_otro_admin(client: TestClient, db, usuario_admin):
    from app.models.usuario import Usuario
    from app.utils.password import hash_password

    otro_admin = Usuario(
        nombre="Otro Admin",
        email="otro-admin@test.com",
        password_hash=hash_password("Admin123!"),
        role="admin",
        activo=True,
    )
    db.add(otro_admin)
    db.commit()
    db.refresh(otro_admin)

    response = client.put(
        f"/api/v1/admin/usuarios/{otro_admin.id}/rol",
        json={"role": "lector"},
        headers=auth_header(usuario_admin),
    )
    assert response.status_code == 200
    assert response.json()["role"] == "lector"


def test_admin_puede_promover_lector_a_admin(
    client: TestClient, usuario_admin, usuario_lector
):
    response = client.put(
        f"/api/v1/admin/usuarios/{usuario_lector.id}/rol",
        json={"role": "admin"},
        headers=auth_header(usuario_admin),
    )
    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_admin_no_puede_desactivarse_a_si_mismo(client: TestClient, usuario_admin):
    response = client.put(
        f"/api/v1/admin/usuarios/{usuario_admin.id}/estado",
        json={"activo": False},
        headers=auth_header(usuario_admin),
    )
    assert response.status_code == 409
