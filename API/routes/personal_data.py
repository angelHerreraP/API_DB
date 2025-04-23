from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from API import models, schemas
from API.database import get_db
from API.utils.dependencies import get_current_user  # Asumimos que tienes esta dependencia
from sqlalchemy import func
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(
    prefix="/personal_data",
    tags=["Personal Data"],
    dependencies=[Depends(get_current_user)],  # Protegemos estas rutas
)

@router.post("/", response_model=schemas.PersonalData)
async def create_personal_data(personal_data: schemas.PersonalDataCreate, db: Session = Depends(get_db)):
    db_personal_data = models.PersonalData(
        usuario_id=personal_data.usuario_id,
        dni=func.pgp_sym_encrypt(personal_data.dni, func.digest(os.getenv("SECRET_KEY"), 'sha256')),
        telefono=func.pgp_sym_encrypt(personal_data.telefono, func.digest(os.getenv("SECRET_KEY"), 'sha256')),
    )
    db.add(db_personal_data)
    db.commit()
    db.refresh(db_personal_data)
    return db_personal_data

@router.get("/{user_id}", response_model=schemas.PersonalData)
async def get_personal_data(user_id: int, db: Session = Depends(get_db)):
    db_personal_data = db.query(models.PersonalData).filter(models.PersonalData.usuario_id == user_id).first()
    if not db_personal_data:
        raise HTTPException(status_code=404, detail="Datos personales no encontrados")
    decrypted_dni = db.scalar(func.pgp_sym_decrypt(db_personal_data.dni, func.digest(os.getenv("SECRET_KEY"), 'sha256'))).decode('utf-8')
    decrypted_telefono = db.scalar(func.pgp_sym_decrypt(db_personal_data.telefono, func.digest(os.getenv("SECRET_KEY"), 'sha256'))).decode('utf-8')
    return schemas.PersonalData(id=db_personal_data.id, usuario_id=db_personal_data.usuario_id, dni=decrypted_dni, telefono=decrypted_telefono)

@router.put("/{user_id}", response_model=schemas.PersonalData)
async def update_personal_data(user_id: int, personal_data: schemas.PersonalDataUpdate, db: Session = Depends(get_db)):
    db_personal_data = db.query(models.PersonalData).filter(models.PersonalData.usuario_id == user_id).first()
    if not db_personal_data:
        raise HTTPException(status_code=404, detail="Datos personales no encontrados")
    if personal_data.dni:
        db_personal_data.dni = func.pgp_sym_encrypt(
            personal_data.dni, func.digest(os.getenv("SECRET_KEY"), 'sha256')
        )
    if personal_data.telefono:
        db_personal_data.telefono = func.pgp_sym_encrypt(
            personal_data.telefono, func.digest(os.getenv("SECRET_KEY"), 'sha256')
        )
    db.commit()
    db.refresh(db_personal_data)
    return db_personal_data