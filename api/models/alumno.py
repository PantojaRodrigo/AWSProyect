from pydantic import BaseModel, Field

class Alumno(BaseModel):
    id: int 
    nombres: str
    apellidos: str
    matricula: str
    promedio: float
    
class CreateAlumno(BaseModel):
    nombres: str
    apellidos: str
    matricula: str
    promedio: float


        