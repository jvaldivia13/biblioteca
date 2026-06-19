from pydantic import BaseModel
from datetime import date
from typing import Optional


class PrestamoCreate(BaseModel):
    libro_id: int


class LibroBasicResponse(BaseModel):
    id: int
    titulo: str
    autor: str

    class Config:
        from_attributes = True


class PrestamoResponse(BaseModel):
    id: int
    usuario_id: int
    libro_id: int
    libro: LibroBasicResponse
    fecha_prestamo: date
    fecha_devolucion_esperada: date
    fecha_devolucion_real: Optional[date]
    estado: str
    vencido: bool

    class Config:
        from_attributes = True


class PrestamosListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[PrestamoResponse]
