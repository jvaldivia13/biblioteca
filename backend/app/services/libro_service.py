from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.libro import Libro
from app.repositories import libro_repo, prestamo_repo
from app.schemas.libro import LibroCreate, LibroUpdate


def crear_libro(db: Session, libro_data: LibroCreate) -> Libro:
    if libro_data.isbn:
        libro_existente = libro_repo.get_libro_by_isbn(db, libro_data.isbn)
        if libro_existente:
            raise HTTPException(status_code=409, detail="ISBN ya está registrado")

    nuevo_libro = Libro(**libro_data.model_dump())
    return libro_repo.create_libro(db, nuevo_libro)


def obtener_libro(db: Session, libro_id: int) -> Libro:
    libro = libro_repo.get_libro_by_id(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


def buscar_libros(
    db: Session,
    q: str | None = None,
    categoria: str | None = None,
    limit: int = 20,
    offset: int = 0,
):
    if limit > 100:
        limit = 100

    return libro_repo.search_libros(db, q, categoria, limit, offset)


def actualizar_libro(db: Session, libro_id: int, libro_data: LibroUpdate) -> Libro:
    libro = libro_repo.get_libro_by_id(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    if libro_data.isbn and libro_data.isbn != libro.isbn:
        libro_existente = libro_repo.get_libro_by_isbn(db, libro_data.isbn)
        if libro_existente:
            raise HTTPException(status_code=409, detail="ISBN ya está registrado")

    update_data = libro_data.model_dump(exclude_unset=True)
    return libro_repo.update_libro(db, libro_id, update_data)


def eliminar_libro(db: Session, libro_id: int) -> None:
    libro = libro_repo.get_libro_by_id(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    prestamos_activos = prestamo_repo.get_prestamos_activos_by_libro(db, libro_id)
    if prestamos_activos > 0:
        raise HTTPException(
            status_code=409, detail="No se puede eliminar: tiene préstamos activos"
        )

    libro_repo.delete_libro(db, libro_id)


def get_disponibles(db: Session, libro_id: int) -> int:
    return libro_repo.get_disponibles(db, libro_id)
