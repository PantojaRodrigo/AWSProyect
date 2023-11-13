import json
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from api.models.alumno import Alumno

from repository import Repository

alumnos_router = APIRouter(
    prefix="/alumnos",
    tags=["alumnos"]
)

alumnosRepo = Repository()

@alumnos_router.get("")
def get_all_alumnos():
    return alumnosRepo.elementos

@alumnos_router.get("/{id}")
def get_alumno_by_id(id: int):
    alumno = alumnosRepo.get_element_by_id(id)
    if alumno is None:
        return JSONResponse({"message": "No alumno found"}, status_code=status.HTTP_404_NOT_FOUND)
    return alumno

@alumnos_router.post("",status_code=201)
def add_alumno(alumno:Alumno):
    if not alumnosRepo.add_element(alumno):
        return JSONResponse({"message": "Alumno could not be added"}, status_code=status.HTTP_409_CONFLICT)

@alumnos_router.put("/{id}")
def update_alumno(id: int,alumno:Alumno):
    if not alumnosRepo.update_element(id,alumno):
        return JSONResponse({"message": "Alumno could not be updated"}, status_code=status.HTTP_409_CONFLICT)

@alumnos_router.delete("/{id}")
def delete_alumno(id: int):
    if not alumnosRepo.delete_element(id):
        return JSONResponse({"message": "No alumno found"}, status_code=status.HTTP_404_NOT_FOUND)




    
