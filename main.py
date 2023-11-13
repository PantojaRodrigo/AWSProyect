from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.routers.alumnos import alumnos_router
from api.routers.profesores import profesores_router

app =  FastAPI()
app.title = "AWSProyect"

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )
    
app.include_router(alumnos_router)
app.include_router(profesores_router)

@app.get("/")
def root():
    return {"message": "Welcome to AWS Proyect by Rodrigo Pantoja"}