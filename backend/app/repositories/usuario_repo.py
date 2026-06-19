from sqlalchemy.orm import Session
from app.models.usuario import Usuario


def get_usuario_by_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def get_usuario_by_id(db: Session, user_id: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == user_id).first()


def create_usuario(db: Session, usuario: Usuario) -> Usuario:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def get_all_usuarios(db: Session, limit: int = 20, offset: int = 0):
    total = db.query(Usuario).count()
    usuarios = db.query(Usuario).offset(offset).limit(limit).all()
    return total, usuarios


def update_usuario_estado(db: Session, user_id: int, activo: bool) -> Usuario | None:
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if usuario:
        usuario.activo = activo
        db.commit()
        db.refresh(usuario)
    return usuario


def update_usuario_rol(db: Session, user_id: int, role: str) -> Usuario | None:
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if usuario:
        usuario.role = role
        db.commit()
        db.refresh(usuario)
    return usuario
