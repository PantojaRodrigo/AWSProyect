from pydantic import BaseModel, Field

class ProfesorRequest(BaseModel):
    numeroEmpleado: int
    nombres: str
    apellidos: str
    horasClase: int