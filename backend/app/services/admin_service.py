from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.usuario import Usuario
from app.models.prestamo import Prestamo
from app.models.libro import Libro
from app.repositories import usuario_repo


def obtener_estadisticas(db: Session) -> dict:
    total_libros = db.query(Libro).count()
    total_usuarios = db.query(Usuario).count()
    prestamos_activos = db.query(Prestamo).filter(
        Prestamo.estado == "activo"
    ).count()

    from datetime import date
    prestamos_vencidos = db.query(Prestamo).filter(
        Prestamo.estado == "activo",
        Prestamo.fecha_devolucion_esperada < date.today()
    ).count()

    libros_disponibles = 0
    for libro in db.query(Libro).all():
        prestados = db.query(func.count(Prestamo.id)).filter(
            Prestamo.libro_id == libro.id,
            Prestamo.estado == "activo"
        ).scalar() or 0
        if libro.stock_total - prestados > 0:
            libros_disponibles += 1

    return {
        "total_libros": total_libros,
        "total_usuarios": total_usuarios,
        "prestamos_activos": prestamos_activos,
        "prestamos_vencidos": prestamos_vencidos,
        "libros_disponibles": libros_disponibles,
    }


def obtener_usuarios(db: Session, limit: int = 20, offset: int = 0):
    return usuario_repo.get_all_usuarios(db, limit, offset)


def cambiar_estado_usuario(
    db: Session, usuario_id: int, activo: bool, current_user_id: int
) -> Usuario:
    usuario = usuario_repo.get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.id == current_user_id and not activo:
        raise HTTPException(
            status_code=409, detail="El admin no puede desactivar su propia cuenta"
        )

    return usuario_repo.update_usuario_estado(db, usuario_id, activo)


def cambiar_rol_usuario(
    db: Session, usuario_id: int, role: str, current_user_id: int
) -> Usuario:
    usuario = usuario_repo.get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.id == current_user_id and usuario.role == "admin" and role != "admin":
        raise HTTPException(
            status_code=409, detail="El admin no puede quitarse su propio rol"
        )

    return usuario_repo.update_usuario_rol(db, usuario_id, role)
