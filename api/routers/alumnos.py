import json
from typing import Annotated
from dbconnection import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter,status,Depends, File, UploadFile
from fastapi.responses import JSONResponse
from api.models.alumno import AlumnoRequest, LoginRequest, SessionValidation
from modelsdb import Alumnos
from awsconfig import s3_client, dynamo_table, sns_topic
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
def upload_profile_picture(id: int,foto: UploadFile, db: db_dependency):
    try:
        ext = foto.content_type.split("/")
        
        ''' if ext[0] != "image":
            print("Error imagen"+ str(ext))
            return JSONResponse({"message": "No es una imagen "}, status_code=status.HTTP_400_BAD_REQUEST) '''
        content_type = foto.content_type if ext[0]=="image" else "image/jpg"
        # Upload the file to to your S3 service
        filename=str(uuid.uuid4())+"."+content_type.split("/")[1]
        
        s3_client.upload_fileobj(foto.file, 'aws-proyecto-bucket',filename,ExtraArgs={"ContentType":content_type})
        
        alumno_model = db.query(Alumnos).filter(Alumnos.id==id).first()
        alumno_model.fotoPerfilUrl = "https://aws-proyecto-bucket.s3.amazonaws.com/" + str(filename)
        db.add(alumno_model)
        db.commit()
    except Exception as ex:
        traceback.print_exc()
        return JSONResponse({"message": "Error al subir imagen"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        foto.file.close()
    return JSONResponse({"fotoPerfilUrl": alumno_model.fotoPerfilUrl}, status_code=status.HTTP_200_OK)
    
    

#Session
@alumnos_router.post("/{id}/session/login")
def create_session(id: int, loginRequest:LoginRequest ,db: db_dependency):
    alumno_model = db.query(Alumnos).filter(Alumnos.id==id).first()
    if alumno_model is None:
        return JSONResponse({"message": "No se encontro al alumno"}, status_code=status.HTTP_404_NOT_FOUND)
    if loginRequest.password != alumno_model.password:
        return JSONResponse({"message": "Contraseña invalida"}, status_code=status.HTTP_400_BAD_REQUEST)
    session_string = generateSession()
    response = dynamo_table.put_item(
        Item={
                'id': str(uuid.uuid4()),
                'fecha': int(time.mktime(datetime.datetime.now().timetuple())),
                'alumnoId': alumno_model.id,
                'active': True,
                'sessionString': session_string,
            }
    )
    return {"sessionString": session_string}


@alumnos_router.post("/{id}/session/verify")
def verify_session(id: int,sessionVal :SessionValidation, db: db_dependency):
    alumno_model = db.query(Alumnos).filter(Alumnos.id==id).first()
    if alumno_model is None:
        return JSONResponse({"message": "No se encontro al alumno"}, status_code=status.HTTP_404_NOT_FOUND)
    response = dynamo_table.scan(
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
    response = dynamo_table.scan(
        FilterExpression=Attr('alumnoId').eq(alumno_model.id) 
        & Attr('sessionString').eq(sessionVal.sessionString)
        & Attr('active').eq(True)
    )
    if len(response["Items"])==0:
        return  JSONResponse({"message": "No se encontro una session activa"}, status_code=status.HTTP_400_BAD_REQUEST)
    item = response["Items"][0]
    item["active"]=False
    dynamo_table.put_item(Item=item) 

@alumnos_router.post("/{id}/email")
def send_sns(id: int,db: db_dependency):
    alumno_model = db.query(Alumnos).filter(Alumnos.id==id).first()
    if alumno_model is None:
        return JSONResponse({"message": "No se encontro al alumno"}, status_code=status.HTTP_404_NOT_FOUND)
    message = f"Las calificaciones del alumno \n{alumno_model.nombres} {alumno_model.apellidos} \n\
          es de {alumno_model.promedio}"
    sns_topic.publish(Message = message)
