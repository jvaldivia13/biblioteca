#!/usr/bin/env python
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal, create_tables
from app.models.usuario import Usuario
from app.models.libro import Libro
from app.utils.password import hash_password


SAMPLE_BOOKS = [
    {
        "titulo": "Cien años de soledad",
        "autor": "Gabriel García Márquez",
        "isbn": "978-0307474728",
        "categoria": "Novela",
        "anio_publicacion": 1967,
        "stock_total": 3,
        "descripcion": "La historia de la familia Buendía en el pueblo de Macondo.",
    },
    {
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "isbn": "978-0132350884",
        "categoria": "Ingeniería de Software",
        "anio_publicacion": 2008,
        "stock_total": 2,
        "descripcion": "Guía de buenas prácticas de programación.",
    },
    {
        "titulo": "El Principito",
        "autor": "Antoine de Saint-Exupéry",
        "isbn": "978-0156012195",
        "categoria": "Literatura",
        "anio_publicacion": 1943,
        "stock_total": 5,
        "descripcion": "Un cuento poético sobre un príncipe de otro planeta.",
    },
    {
        "titulo": "Python Crash Course",
        "autor": "Eric Matthes",
        "isbn": "978-1718502703",
        "categoria": "Programación",
        "anio_publicacion": 2023,
        "stock_total": 4,
        "descripcion": "Aprende Python desde cero con proyectos prácticos.",
    },
    {
        "titulo": "El Quijote",
        "autor": "Miguel de Cervantes",
        "isbn": "978-8408089094",
        "categoria": "Novela",
        "anio_publicacion": 1605,
        "stock_total": 2,
        "descripcion": "Las aventuras de Don Quijote y Sancho Panza.",
    },
]


def seed():
    create_tables()
    db = SessionLocal()
    try:
        if not db.query(Usuario).filter_by(email="admin@biblioapp.pe").first():
            admin = Usuario(
                nombre="Administrador",
                email="admin@biblioapp.pe",
                password_hash=hash_password("Admin123!"),
                role="admin",
                activo=True,
            )
            db.add(admin)
            print("Admin creado: admin@biblioapp.pe / Admin123!")

        creados = 0
        actualizados = 0
        for libro_data in SAMPLE_BOOKS:
            libro = db.query(Libro).filter_by(isbn=libro_data["isbn"]).first()
            if libro:
                for key, value in libro_data.items():
                    setattr(libro, key, value)
                actualizados += 1
            else:
                db.add(Libro(**libro_data))
                creados += 1

        db.commit()
        print(f"{creados} libros de ejemplo creados")
        print(f"{actualizados} libros de ejemplo actualizados")
        print("\nSeed completado exitosamente")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
