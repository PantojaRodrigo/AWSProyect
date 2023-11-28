from typing import Optional
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Float
from dbconnection import Base

class Alumnos(Base):
    __tablename__ = "alumnos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombres: Mapped[str] = mapped_column(String(128))
    apellidos : Mapped[str] = mapped_column(String(128))
    matricula : Mapped[str] = mapped_column(String(16),unique=True)
    promedio : Mapped[float] = mapped_column(Float)
    password : Mapped[str] = mapped_column(String(128))
    fotoPerfilUrl : Mapped[Optional[str]] = mapped_column(String(128))
    
    def as_dict(self):
           return {c.name: getattr(self, c.name) for c in self.__table__.columns}

   
class Profesores(Base):
    __tablename__ = "profesores"
    id : Mapped[int] = mapped_column(primary_key=True)
    nombres : Mapped[str] = mapped_column(String(128))
    apellidos : Mapped[str] = mapped_column(String(128))
    numeroEmpleado : Mapped[int] = mapped_column(Integer,unique=True)
    horasClase : Mapped[int] = mapped_column(Integer)
    
    def as_dict(self):
           return {c.name: getattr(self, c.name) for c in self.__table__.columns}
