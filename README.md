# AWSProyect
Proyecto para la materia AWS cloud academy foundations

## Crear Python Envivorement
    python3 -m venv venv
## Seleccionar Envivorement en VSC
## Activar  Envivorement
    venv/Scripts/activate
## Instalar dependencias/librerias
    pip install -r requirements.txt 
## Correr uvicorn
    uvicorn main:app --port 8080
## Correr uvicorn en AWS:
    nohup uvicorn main:app --port 8080 &

