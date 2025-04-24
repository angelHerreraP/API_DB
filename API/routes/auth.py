from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from API import models, schemas
from API.database import get_db
from API.utils import hashing, jwt
from API.utils.dependencies import get_current_user  # Asumimos que tienes esta dependencia
from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Nombre de usuario ya registrado")
    hashed_password = hashing.hash_password(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed_password,
        rol_id=user.rol_id  # Usa el rol_id recibido
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
async def login_user(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    ip_address = request.client.host

    if not user or not hashing.verify_password(form_data.password, user.password_hash):
        audit_log = models.AuditLog(
            usuario_id=user.id if user else None,
            accion="login_fallido",
            fecha=datetime.utcnow(),
            ip=ip_address
        )
        db.add(audit_log)
        db.commit()
        raise HTTPException(status_code=400, detail="Nombre de usuario o contraseña incorrectos")

    access_token = jwt.create_access_token(data={"sub": user.username})

    audit_log = models.AuditLog(
        usuario_id=user.id,
        accion="login_exitoso",
        fecha=datetime.utcnow(),
        ip=ip_address
    )
    db.add(audit_log)
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.User)
async def get_current_user_route(current_user: models.User = Depends(get_current_user)):
    return current_user