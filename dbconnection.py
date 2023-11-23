from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker, DeclarativeBase

SQALCHEMY_DATABASE_URL="mysql+mysqlconnector://admin:Admin123@db-proyect-aws.c10b9kpab8at.us-east-1.rds.amazonaws.com:3306/proyectodb"


engine = create_engine(SQALCHEMY_DATABASE_URL,echo=False)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass