from pydantic import BaseModel
from datetime import datetime


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    role: str
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
    role: str
