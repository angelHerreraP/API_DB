from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from API import models, schemas
from API.database import get_db
from API.utils.dependencies import get_current_user  # Asumimos que tienes esta dependencia

router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
    dependencies=[Depends(get_current_user)],  # Protegemos estas rutas
)

@router.get("/", response_model=List[schemas.AuditLog])
async def get_audit_logs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    audit_logs = db.query(models.AuditLog).offset(skip).limit(limit).all()
    return audit_logs

@router.get("/{audit_id}", response_model=schemas.AuditLog)
async def get_audit_log(audit_id: int, db: Session = Depends(get_db)):
    db_audit_log = db.query(models.AuditLog).filter(models.AuditLog.id == audit_id).first()
    if db_audit_log is None:
        raise HTTPException(status_code=404, detail="Registro de auditoría no encontrado")
    return db_audit_log

# Podrías añadir más rutas para filtrar o buscar registros de auditoría