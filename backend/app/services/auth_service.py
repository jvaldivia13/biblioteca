from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.repositories import usuario_repo
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token


def registrar_usuario(db: Session, nombre: str, email: str, password: str) -> Usuario:
    usuario_existente = usuario_repo.get_usuario_by_email(db, email)
    if usuario_existente:
        raise HTTPException(status_code=409, detail="Email ya está en uso")

    password_hash = hash_password(password)
    nuevo_usuario = Usuario(
        nombre=nombre, email=email, password_hash=password_hash, role="lector"
    )

    return usuario_repo.create_usuario(db, nuevo_usuario)


def login_usuario(db: Session, email: str, password: str) -> dict:
    usuario = usuario_repo.get_usuario_by_email(db, email)

    if not usuario or not verify_password(password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not usuario.activo:
        raise HTTPException(status_code=403, detail="Cuenta desactivada")

    access_token = create_access_token(
        {"user_id": usuario.id, "email": usuario.email, "role": usuario.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": usuario.role,
    }
