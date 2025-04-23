from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from API import models, schemas
from API.database import get_db
from API.utils.dependencies import get_current_user  # Asumimos que tienes esta dependencia

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    dependencies=[Depends(get_current_user)],  # Protegemos estas rutas
)

@router.post("/", response_model=schemas.Role)
async def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = db.query(models.Role).filter(models.Role.nombre == role.nombre).first()
    if db_role:
        raise HTTPException(status_code=400, detail="El rol ya existe")
    db_role = models.Role(nombre=role.nombre)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/", response_model=List[schemas.Role])
async def get_roles(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    roles = db.query(models.Role).offset(skip).limit(limit).all()
    return roles

@router.get("/{role_id}", response_model=schemas.Role)
async def get_role(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_role

@router.put("/{role_id}", response_model=schemas.Role)
async def update_role(role_id: int, role: schemas.RoleUpdate, db: Session = Depends(get_db)):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db_role.nombre = role.nombre
    db.commit()
    db.refresh(db_role)
    return db_role

@router.delete("/{role_id}", response_model=schemas.Message)
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(db_role)
    db.commit()
    return {"message": f"Rol con ID {role_id} eliminado"}