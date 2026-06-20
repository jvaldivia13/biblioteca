# 📚 BiblioApp v1.0

Sistema de Gestión de Biblioteca desarrollado con FastAPI, SQLite y JavaScript Vanilla.

## Características

- ✅ Autenticación con JWT
- ✅ CRUD de Libros
- ✅ Sistema de Préstamos
- ✅ Gestión de Usuarios (Admin)
- ✅ Dashboard de Estadísticas
- ✅ Interfaz Responsive

## Stack Tecnológico

**Backend:**
- Python 3.11+
- FastAPI
- SQLAlchemy 2.0
- Pydantic
- SQLite

**Frontend:**
- HTML5
- CSS3
- JavaScript ES2022+

## Instalación

### Requisitos
- Python 3.11+
- pip
- virtualenv (opcional pero recomendado)

### Backend

1. Crea un ambiente virtual:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus valores
```

En Windows PowerShell:
```powershell
Copy-Item .env.example .env
```

4. Ejecuta el servidor:
```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

### Frontend

El frontend es una aplicación estática. Puedes servirlo de dos formas:

**Opción 1: Python SimpleHTTPServer**
```bash
cd frontend
python -m http.server 3000
```

**Opción 2: Con Docker Compose (recomendado)**
```bash
docker-compose up
```

## Configuración

### Variables de Entorno (.env)

```env
DATABASE_URL=sqlite:///./biblioapp.db
JWT_SECRET_KEY=tu_clave_secreta_aqui
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
DEBUG=false
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Testing

Ejecuta los tests con pytest:

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

Para ver el reporte de cobertura:

```bash
python -m pytest tests/ -v --cov=app --cov-report=html
```

## API Documentation

Una vez que el servidor está corriendo, accede a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints Principales

### Autenticación
- `POST /api/v1/auth/register` - Registrar usuario
- `POST /api/v1/auth/login` - Login

### Libros
- `GET /api/v1/libros` - Listar libros
- `GET /api/v1/libros/{id}` - Detalle del libro
- `POST /api/v1/libros` - Crear libro (admin)
- `PUT /api/v1/libros/{id}` - Actualizar libro (admin)
- `DELETE /api/v1/libros/{id}` - Eliminar libro (admin)

### Préstamos
- `POST /api/v1/prestamos` - Solicitar préstamo
- `PUT /api/v1/prestamos/{id}/devolver` - Registrar devolución
- `GET /api/v1/prestamos/mis-prestamos` - Mis préstamos
- `GET /api/v1/prestamos` - Todos los préstamos (admin)

### Admin
- `GET /api/v1/admin/stats` - Estadísticas
- `GET /api/v1/admin/usuarios` - Listar usuarios
- `PUT /api/v1/admin/usuarios/{id}/estado` - Cambiar estado
- `PUT /api/v1/admin/usuarios/{id}/rol` - Cambiar rol

## Estructura del Proyecto

```
biblioapp/
├── backend/
│   ├── app/
│   │   ├── models/        # Modelos SQLAlchemy
│   │   ├── schemas/       # Esquemas Pydantic
│   │   ├── routers/       # Endpoints
│   │   ├── services/      # Lógica de negocio
│   │   ├── repositories/  # Acceso a datos
│   │   ├── utils/         # Utilidades
│   │   ├── main.py        # App principal
│   │   ├── config.py      # Configuración
│   │   └── database.py    # BD
│   ├── tests/             # Tests
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── mis-prestamos.html
│   ├── admin/
│   ├── css/
│   └── js/
│
├── docker-compose.yml
└── README.md
```

## Usuarios de Prueba

Al instalar por primera vez, crea un usuario admin:

```python
python backend/scripts/seed.py
```

Usuario por defecto:
- Email: `admin@biblioapp.pe`
- Contraseña: `Admin123!`

## Despliegue

### Con Docker Compose

```bash
docker-compose up -d
```

### En Producción

**Backend (Render.com):**
1. Conectar repo GitHub a Render
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Agregar disco persistente en `/app/data`

**Frontend (Vercel/Netlify):**
- Hacer deploy de la carpeta `/frontend`

## Desarrollo

### Pre-requisitos para Contribuir
- Conocimiento de Python, FastAPI, SQL y JavaScript
- Git

### Pasos para Desarrollar
1. Clona el repositorio
2. Crea una rama: `git checkout -b feature/mi-feature`
3. Haz commits descriptivos
4. Push a la rama: `git push origin feature/mi-feature`
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Contacto

Para preguntas o sugerencias, contacta al equipo de desarrollo.

---

**BiblioApp v1.0 — Junio 2026**
