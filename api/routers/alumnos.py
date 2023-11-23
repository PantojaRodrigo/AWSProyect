import json
from typing import Annotated
from dbconnection import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter,status,Depends
from fastapi.responses import JSONResponse
from api.models.alumno import AlumnoRequest
from modelsdb import Alumnos

alumnos_router = APIRouter(
    prefix="/alumnos",
    tags=["alumnos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@alumnos_router.get("")
async def get_all_alumnos(db: db_dependency):
    return db.query(Alumnos).all()

@alumnos_router.get("/{id}")
def get_alumno_by_id(id: int,db: db_dependency):
    alumno = db.query(Alumnos).filter(Alumnos.id == id).first()
    if alumno is None:
        return JSONResponse({"message": "No se encontro al alumno"}, status_code=status.HTTP_404_NOT_FOUND)
    return alumno

@alumnos_router.post("",status_code=201)
def add_alumno(alumno:AlumnoRequest,db: db_dependency):
    alumno_model =  Alumnos(**alumno.model_dump())
    db.add(alumno_model)
    db.commit()
    #return JSONResponse({"message": "Alumno could not be added"}, status_code=status.HTTP_409_CONFLICT)

@alumnos_router.put("/{id}")
def update_alumno(id: int,alumno:AlumnoRequest,db: db_dependency):
    alumno_model = db.query(Alumnos).filter(Alumnos.id==id).first()
    if alumno_model is None:
        return JSONResponse({"message": "No se encontro al alumno"}, status_code=status.HTTP_404_NOT_FOUND)
    alumno_model.nombres = alumno.nombres
    alumno_model.apellidos = alumno.apellidos
    alumno_model.matricula = alumno.matricula
    alumno_model.promedio = alumno.promedio
    alumno_model.password = alumno.password
    
    db.add(alumno_model)
    db.commit()
    

@alumnos_router.delete("/{id}")
def delete_alumno(id: int,db: db_dependency):
    alumno_model = db.query(Alumnos).filter(Alumnos.id==id).first()
    if alumno_model is None:
        return JSONResponse({"message": "No se encontro al alumno"}, status_code=status.HTTP_404_NOT_FOUND)
    db.delete(alumno_model)
    db.commit()
