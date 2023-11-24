import json
from typing import Annotated
from dbconnection import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter,status,Depends, File, UploadFile
from fastapi.responses import JSONResponse
from api.models.alumno import AlumnoRequest, LoginRequest, SessionValidation
from modelsdb import Alumnos
from awsconfig import s3_client, dynamo_client
from boto3.dynamodb.conditions import Attr
import uuid, random,string, traceback, datetime,time, json


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
    return JSONResponse(alumno_model.as_dict(), status_code=status.HTTP_201_CREATED)

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
    
@alumnos_router.post("/{id}/fotoPerfil")
def upload_profile_picture(id: int,file: UploadFile, db: db_dependency):
    try:
        ext = file.content_type.split("/")
        if ext[0] != "image":
            return JSONResponse({"message": "No es una imagen "}, status_code=status.HTTP_400_BAD_REQUEST)
        # Upload the file to to your S3 service
        filename=str(uuid.uuid4())+"."+ext[1]
        s3_client.upload_fileobj(file.file, 'aws-proyecto-bucket',filename,ExtraArgs={"ContentType":str(file.content_type)})
        
        alumno_model = db.query(Alumnos).filter(Alumnos.id==id).first()
        alumno_model.fotoPerfilUrl = "https://aws-proyecto-bucket.s3.amazonaws.com/" + str(filename)
        db.add(alumno_model)
        db.commit()
        
    except Exception as ex:
        traceback.print_exc()
        return JSONResponse({"message": "Error al subir imagen"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        file.file.close()
    JSONResponse({"filename": str(file.filename)}, status_code=status.HTTP_200_OK)

@alumnos_router.post("/{id}/session/login")
def create_session(id: int, loginRequest:LoginRequest ,db: db_dependency):
    alumno_model = db.query(Alumnos).filter(Alumnos.id==id).first()
    if alumno_model is None:
        return JSONResponse({"message": "No se encontro al alumno"}, status_code=status.HTTP_404_NOT_FOUND)
    if loginRequest.password != alumno_model.password:
        return JSONResponse({"message": "Contraseña invalida"}, status_code=status.HTTP_400_BAD_REQUEST)
    session_table = dynamo_client.Table("sesiones-alumnos")
    response = session_table.put_item(
        Item={
                'id': str(uuid.uuid4()),
                'fecha': int(time.mktime(datetime.datetime.now().timetuple())),
                'alumnoId': alumno_model.id,
                'active': True,
                'sessionString': generateSession(),
            }
    )

@alumnos_router.post("/{id}/session/verify")
def verify_session(id: int,sessionVal :SessionValidation, db: db_dependency):
    alumno_model = db.query(Alumnos).filter(Alumnos.id==id).first()
    if alumno_model is None:
        return JSONResponse({"message": "No se encontro al alumno"}, status_code=status.HTTP_404_NOT_FOUND)
    session_table = dynamo_client.Table("sesiones-alumnos")
    response = session_table.scan(
        FilterExpression=Attr('alumnoId').eq(alumno_model.id) 
        & Attr('sessionString').eq(sessionVal.sessionString)
        & Attr('active').eq(True)
    )
    if len(response["Items"])==0:
        return  JSONResponse({"message": "Session invalida"}, status_code=status.HTTP_400_BAD_REQUEST)  
    
def generateSession():
    letters = string.ascii_lowercase+string.ascii_uppercase+string.digits            
    return ''.join(random.choice(letters) for i in range(128))

@alumnos_router.post("/{id}/session/logout")
def delete_session(id: int,sessionVal :SessionValidation, db: db_dependency):
    alumno_model = db.query(Alumnos).filter(Alumnos.id==id).first()
    if alumno_model is None:
        return JSONResponse({"message": "No se encontro al alumno"}, status_code=status.HTTP_404_NOT_FOUND)
    session_table = dynamo_client.Table("sesiones-alumnos")
    response = session_table.scan(
        FilterExpression=Attr('alumnoId').eq(alumno_model.id) 
        & Attr('sessionString').eq(sessionVal.sessionString)
        & Attr('active').eq(True)
    )
    if len(response["Items"])==0:
        return  JSONResponse({"message": "No se encontro una session activa"}, status_code=status.HTTP_400_BAD_REQUEST)
    item = response["Items"][0]
    item["active"]=False
    session_table.put_item(Item=item) 

