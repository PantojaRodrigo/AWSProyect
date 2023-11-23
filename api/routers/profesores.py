import json
from typing import Annotated
from dbconnection import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter,status,Depends
from fastapi.responses import JSONResponse
from api.models.profesor import ProfesorRequest
from modelsdb import Profesores

profesores_router = APIRouter(
    prefix="/profesores",
    tags=["profesores"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@profesores_router.get("")
def get_all_profesores(db: db_dependency):
    return db.query(Profesores).all()

@profesores_router.get("/{id}")
def get_profesor_by_id(id: int,db: db_dependency):
    profesor = db.query(Profesores).filter(Profesores.id == id).first()
    if profesor is None:
        return JSONResponse({"message": "No Profesor found"}, status_code=status.HTTP_404_NOT_FOUND)
    return profesor

@profesores_router.post("",status_code=201)
def add_profesor(profesor:ProfesorRequest,db: db_dependency):
    profesor_model =  Profesores(**profesor.model_dump())
    
    db.add(profesor_model)
    db.commit()
        
@profesores_router.put("/{id}")
def update_profesor(id: int,profesor:ProfesorRequest,db: db_dependency):
    profesor_model = db.query(Profesores).filter(Profesores.id==id).first()
    if profesor_model is None:
        return JSONResponse({"message": "No se encontro al profesor"}, status_code=status.HTTP_404_NOT_FOUND)
    profesor_model.nombres = profesor.nombres
    profesor_model.apellidos = profesor.apellidos
    profesor_model.numeroEmpleado = profesor.numeroEmpleado
    profesor_model.horasClase = profesor.horasClase
    
    db.add(profesor_model)
    db.commit()
    
@profesores_router.delete("/{id}")
def delete_profesor(id: int,db: db_dependency):
    profesor_model = db.query(Profesores).filter(Profesores.id==id).first()
    if profesor_model is None:
        return JSONResponse({"message": "No se encontro al profesor"}, status_code=status.HTTP_404_NOT_FOUND)
    db.delete(profesor_model)
    db.commit()
