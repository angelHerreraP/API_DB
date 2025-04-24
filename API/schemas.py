from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RoleBase(BaseModel):
    nombre: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):  # ¡Añade esta clase!
    nombre: Optional[str] = None

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True  # Actualizado para Pydantic v2

class UserBase(BaseModel):
    username: str
    rol_id: int

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    password: Optional[str] = None
    rol_id: Optional[int] = None

class User(UserBase):
    id: int
    role: Role

    class Config:
        from_attributes = True  # Actualizado para Pydantic v2

class AuditLogBase(BaseModel):
    usuario_id: int
    accion: str
    ip: str

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    id: int
    fecha: datetime
    usuario: User

    class Config:
        from_attributes = True  # Actualizado para Pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Message(BaseModel):
    message: str