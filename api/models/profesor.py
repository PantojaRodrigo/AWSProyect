from pydantic import BaseModel, Field

class Profesor(BaseModel):
    id: int
    numeroEmpleado: int
    nombres: str
    apellidos: str
    horasClase: int
    

    
    