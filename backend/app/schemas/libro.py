from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class LibroCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    autor: str = Field(..., min_length=1, max_length=150)
    isbn: Optional[str] = None
    categoria: str = Field(..., min_length=1, max_length=80)
    anio_publicacion: Optional[int] = Field(None, ge=1000, le=2100)
    stock_total: int = Field(1, ge=1)
    descripcion: Optional[str] = None


class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    isbn: Optional[str] = None
    categoria: Optional[str] = None
    anio_publicacion: Optional[int] = None
    stock_total: Optional[int] = Field(None, ge=0)
    descripcion: Optional[str] = None


class LibroResponse(LibroCreate):
    id: int
    disponibles: int
    created_at: datetime

    class Config:
        from_attributes = True


class LibrosListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[LibroResponse]
