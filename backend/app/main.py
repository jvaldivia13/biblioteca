from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_tables
from app.routers import auth, libros, prestamos, admin

app = FastAPI(
    title="BiblioApp API",
    description="Sistema de Gestión de Biblioteca",
    version="1.0.0",
    docs_url="/docs",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(libros.router, prefix="/api/v1/libros", tags=["Libros"])
app.include_router(prestamos.router, prefix="/api/v1/prestamos", tags=["Préstamos"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def root():
    return {
        "message": "BiblioApp API v1.0",
        "docs": "http://localhost:8000/docs",
    }
