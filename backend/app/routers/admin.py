from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario import (
    UsuarioResponse,
    UsuariosListResponse,
    UsuarioEstadoUpdate,
    UsuarioRolUpdate,
)
from app.services import admin_service
from app.utils.dependencies import require_admin
from app.models.usuario import Usuario

router = APIRouter()


@router.get("/stats")
def obtener_estadisticas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    return admin_service.obtener_estadisticas(db)


@router.get("/usuarios", response_model=UsuariosListResponse)
def listar_usuarios(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    total, items = admin_service.obtener_usuarios(db, limit, offset)
    return UsuariosListResponse(total=total, items=items)


@router.put("/usuarios/{id}/estado", response_model=UsuarioResponse)
def cambiar_estado(
    id: int,
    request: UsuarioEstadoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    return admin_service.cambiar_estado_usuario(db, id, request.activo, current_user.id)


@router.put("/usuarios/{id}/rol", response_model=UsuarioResponse)
def cambiar_rol(
    id: int,
    request: UsuarioRolUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    return admin_service.cambiar_rol_usuario(db, id, request.role, current_user.id)
