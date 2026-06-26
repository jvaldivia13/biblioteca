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
        "titulo": "Cien anos de soledad",
        "autor": "Gabriel Garcia Marquez",
        "isbn": "978-0307474728",
        "categoria": "Novela",
        "anio_publicacion": 1967,
        "stock_total": 3,
        "descripcion": "La historia de la familia Buendia en el pueblo de Macondo.",
    },
    {
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "isbn": "978-0132350884",
        "categoria": "Ingenieria de Software",
        "anio_publicacion": 2008,
        "stock_total": 2,
        "descripcion": "Guia de buenas practicas de programacion.",
    },
    {
        "titulo": "El Principito",
        "autor": "Antoine de Saint-Exupery",
        "isbn": "978-0156012195",
        "categoria": "Literatura",
        "anio_publicacion": 1943,
        "stock_total": 5,
        "descripcion": "Un cuento poetico sobre un principe de otro planeta.",
    },
    {
        "titulo": "Python Crash Course",
        "autor": "Eric Matthes",
        "isbn": "978-1718502703",
        "categoria": "Programacion",
        "anio_publicacion": 2023,
        "stock_total": 4,
        "descripcion": "Aprende Python desde cero con proyectos practicos.",
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
    {
        "titulo": "Breve historia del tiempo",
        "autor": "Stephen Hawking",
        "isbn": "978-0553380163",
        "categoria": "Ciencia",
        "anio_publicacion": 1988,
        "stock_total": 3,
        "descripcion": "Una introduccion accesible al universo, el tiempo y los agujeros negros.",
    },
    {
        "titulo": "Sapiens",
        "autor": "Yuval Noah Harari",
        "isbn": "978-0062316110",
        "categoria": "Historia",
        "anio_publicacion": 2011,
        "stock_total": 4,
        "descripcion": "Un recorrido por la evolucion cultural de la humanidad.",
    },
    {
        "titulo": "Meditaciones",
        "autor": "Marco Aurelio",
        "isbn": "978-0140449334",
        "categoria": "Filosofia",
        "anio_publicacion": 1800,
        "stock_total": 2,
        "descripcion": "Reflexiones estoicas sobre virtud, disciplina y vida publica.",
    },
    {
        "titulo": "Pedagogia del oprimido",
        "autor": "Paulo Freire",
        "isbn": "978-0826412768",
        "categoria": "Educacion",
        "anio_publicacion": 1968,
        "stock_total": 3,
        "descripcion": "Obra clave sobre educacion critica y transformacion social.",
    },
    {
        "titulo": "Pensar rapido, pensar despacio",
        "autor": "Daniel Kahneman",
        "isbn": "978-0374533557",
        "categoria": "Psicologia",
        "anio_publicacion": 2011,
        "stock_total": 3,
        "descripcion": "Analisis de los sistemas de pensamiento y sesgos cognitivos.",
    },
    {
        "titulo": "La riqueza de las naciones",
        "autor": "Adam Smith",
        "isbn": "978-0553585971",
        "categoria": "Economia",
        "anio_publicacion": 1776,
        "stock_total": 2,
        "descripcion": "Texto fundamental sobre mercados, division del trabajo y comercio.",
    },
    {
        "titulo": "Historia del arte",
        "autor": "E. H. Gombrich",
        "isbn": "978-0714832470",
        "categoria": "Arte",
        "anio_publicacion": 1950,
        "stock_total": 2,
        "descripcion": "Panorama claro de movimientos, obras y artistas esenciales.",
    },
    {
        "titulo": "Designing Data-Intensive Applications",
        "autor": "Martin Kleppmann",
        "isbn": "978-1449373320",
        "categoria": "Tecnologia",
        "anio_publicacion": 2017,
        "stock_total": 3,
        "descripcion": "Principios para crear sistemas de datos confiables y escalables.",
    },
    {
        "titulo": "Harry Potter y la piedra filosofal",
        "autor": "J. K. Rowling",
        "isbn": "978-8478884452",
        "categoria": "Fantasia",
        "anio_publicacion": 1997,
        "stock_total": 5,
        "descripcion": "El inicio de la saga del joven mago en Hogwarts.",
    },
    {
        "titulo": "Donde viven los monstruos",
        "autor": "Maurice Sendak",
        "isbn": "978-0064431781",
        "categoria": "Infantil",
        "anio_publicacion": 1963,
        "stock_total": 4,
        "descripcion": "Clasico ilustrado sobre imaginacion, enojo y regreso al hogar.",
    },
    {
        "titulo": "Veinte poemas de amor y una cancion desesperada",
        "autor": "Pablo Neruda",
        "isbn": "978-0307742711",
        "categoria": "Poesia",
        "anio_publicacion": 1924,
        "stock_total": 3,
        "descripcion": "Coleccion poetica sobre amor, deseo y melancolia.",
    },
    {
        "titulo": "Steve Jobs",
        "autor": "Walter Isaacson",
        "isbn": "978-1451648539",
        "categoria": "Biografia",
        "anio_publicacion": 2011,
        "stock_total": 2,
        "descripcion": "Biografia del cofundador de Apple basada en entrevistas extensas.",
    },
    {
        "titulo": "Principios de medicina interna",
        "autor": "Dennis Kasper",
        "isbn": "978-1264268504",
        "categoria": "Medicina",
        "anio_publicacion": 2022,
        "stock_total": 2,
        "descripcion": "Referencia clinica para diagnostico y tratamiento en medicina interna.",
    },
    {
        "titulo": "Teoria pura del derecho",
        "autor": "Hans Kelsen",
        "isbn": "978-9706131728",
        "categoria": "Derecho",
        "anio_publicacion": 1934,
        "stock_total": 2,
        "descripcion": "Exposicion teorica sobre la estructura normativa del derecho.",
    },
    {
        "titulo": "Arquitectura: forma, espacio y orden",
        "autor": "Francis D. K. Ching",
        "isbn": "978-1118745083",
        "categoria": "Arquitectura",
        "anio_publicacion": 1979,
        "stock_total": 3,
        "descripcion": "Fundamentos visuales para comprender composicion arquitectonica.",
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
