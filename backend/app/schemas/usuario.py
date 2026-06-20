from typing import Literal

from pydantic import BaseModel
from datetime import datetime


Role = Literal["admin", "lector"]


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    role: Role
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UsuariosListResponse(BaseModel):
    total: int
    items: list[UsuarioResponse]


class UsuarioEstadoUpdate(BaseModel):
    activo: bool


class UsuarioRolUpdate(BaseModel):
    role: Role
