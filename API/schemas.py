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
        orm_mode = True

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
        orm_mode = True

class PersonalDataBase(BaseModel):
    usuario_id: int
    dni: str
    telefono: str

class PersonalDataCreate(PersonalDataBase):
    pass

class PersonalData(PersonalDataBase):
    id: int

    class Config:
        orm_mode = True

class PersonalDataUpdate(BaseModel):
    dni: Optional[str] = None
    telefono: Optional[str] = None

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
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Message(BaseModel):
    message: str