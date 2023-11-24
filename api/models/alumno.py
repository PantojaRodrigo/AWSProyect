from pydantic import BaseModel, Field

class AlumnoRequest(BaseModel):
    nombres: str
    apellidos: str
    matricula: str
    promedio: float
    password: str    
    
class LoginRequest(BaseModel):
    password: str    
    
class SessionValidation(BaseModel):
    sessionString: str  