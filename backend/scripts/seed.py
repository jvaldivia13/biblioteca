#!/usr/bin/env python
import sys
sys.path.insert(0, '..')

from app.database import SessionLocal, create_tables
from app.models.usuario import Usuario
from app.models.libro import Libro
from app.utils.password import hash_password


def seed():
    create_tables()
    db = SessionLocal()

    # Admin por defecto
    if not db.query(Usuario).filter_by(email="admin@biblioapp.pe").first():
        admin = Usuario(
            nombre="Administrador",
            email="admin@biblioapp.pe",
            password_hash=hash_password("Admin123!"),
            role="admin",
            activo=True,
        )
        db.add(admin)
        print("✅ Admin creado: admin@biblioapp.pe / Admin123!")

    # Libros de ejemplo
    if db.query(Libro).count() == 0:
        libros = [
            Libro(
                titulo="Cien años de soledad",
                autor="Gabriel García Márquez",
                isbn="978-0307474728",
                categoria="Novela",
                anio_publicacion=1967,
                stock_total=3,
                descripcion="La historia de la familia Buendía en el pueblo de Macondo.",
            ),
            Libro(
                titulo="Clean Code",
                autor="Robert C. Martin",
                isbn="978-0132350884",
                categoria="Ingeniería de Software",
                anio_publicacion=2008,
                stock_total=2,
                descripcion="Guía de buenas prácticas de programación.",
            ),
            Libro(
                titulo="El Principito",
                autor="Antoine de Saint-Exupéry",
                isbn="978-0156012195",
                categoria="Literatura",
                anio_publicacion=1943,
                stock_total=5,
                descripcion="Un cuento poético sobre un príncipe de otro planeta.",
            ),
            Libro(
                titulo="Python Crash Course",
                autor="Eric Matthes",
                isbn="978-1718502703",
                categoria="Programación",
                anio_publicacion=2023,
                stock_total=4,
                descripcion="Aprende Python desde cero con proyectos prácticos.",
            ),
            Libro(
                titulo="El Quijote",
                autor="Miguel de Cervantes",
                isbn="978-8408089094",
                categoria="Novela",
                anio_publicacion=1605,
                stock_total=2,
                descripcion="Las aventuras de Don Quijote y Sancho Panza.",
            ),
        ]
        db.add_all(libros)
        print("✅ 5 libros de ejemplo creados")

    db.commit()
    db.close()
    print("\n✅ Seed completado exitosamente")


if __name__ == "__main__":
    seed()
