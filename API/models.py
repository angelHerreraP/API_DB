from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from API.database import Base  # Importa Base desde tu archivo database.py

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "seguridad"}  # Especifica el esquema

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    usuarios = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "seguridad"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("seguridad.roles.id"))
    role = relationship("Role", back_populates="usuarios")
    auditoria = relationship("AuditLog", back_populates="usuario")

class AuditLog(Base):
    __tablename__ = "auditoria"
    __table_args__ = {"schema": "seguridad"}

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("seguridad.usuarios.id"))
    usuario = relationship("User", back_populates="auditoria")
    accion = Column(String(100))
    fecha = Column(TIMESTAMP, default=datetime.utcnow)
    ip = Column(String(45))