import json
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from api.models.alumno import Alumno
from api.models.profesor import Profesor

from repository import Repository

profesores_router = APIRouter(
    prefix="/profesores",
    tags=["profesores"]
)

profesoresRepo = Repository()

@profesores_router.get("")
def get_all_profesores():
    return profesoresRepo.elementos

@profesores_router.get("/{id}")
def get_profesor_by_id(id: int):
    profesor = profesoresRepo.get_element_by_id(id)
    if profesor is None:
        return JSONResponse({"message": "No Profesor found"}, status_code=status.HTTP_404_NOT_FOUND)
    return profesor

@profesores_router.post("",status_code=201)
def add_profesor(profesor:Profesor):
    if not profesoresRepo.add_element(profesor):
        return JSONResponse({"message": "Profesor could not be added"}, status_code=status.HTTP_409_CONFLICT)

@profesores_router.put("/{id}")
def update_profesor(id: int,profesor:Profesor):
    if not profesoresRepo.update_element(id,profesor):
        return JSONResponse({"message": "Profesor could not be updated"}, status_code=status.HTTP_409_CONFLICT)

@profesores_router.delete("/{id}")
def delete_profesor(id: int):
    if not profesoresRepo.delete_element(id):
        return JSONResponse({"message": "Profesor could not be removed"}, status_code=status.HTTP_404_NOT_FOUND)

