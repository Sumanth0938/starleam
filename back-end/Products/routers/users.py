from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,Path
from typing import Annotated
from models import Users
from database import SessionLocal
import models
from starlette import status
from pydantic import BaseModel,Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix = '/users',
    tags=['users']
)

class PasswordRequest(BaseModel):
    password:str
    new_password:str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session,Depends(get_db)]
user_dependancy = Annotated[dict,Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')


@router.get('/current_user',status_code=status.HTTP_200_OK)
def get_current_user_details(user:user_dependancy,db:db_dependancy):

    if user is None:
        raise HTTPException(status_code=401,detail='Authentication is failed')

    data = db.query(Users).filter(Users.id == user.get('user_id')).first()

    return {"message": "successful", "data": data, "status": status.HTTP_200_OK}

@router.put('/change_password',status_code=status.HTTP_204_NO_CONTENT)
def change_password(user:user_dependancy,db:db_dependancy,password_model:PasswordRequest):

    if user is None:
        raise HTTPException(status_code=401,detail='Authentication is failed')

    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()
    if not bcrypt_context.verify(password_model.password,user_model.hashed_password):
        raise HTTPException(status_code=401,detail='password is wrong')

    user_model.hashed_password = bcrypt_context.hash(password_model.new_password)

    return {"message": "password change  sucessfully",  "status": status.HTTP_200_OK}

    db.add(user_model)
    db.commit()

@router.get('/all_users')
def get_all_users_data(db:db_dependancy):

    data= db.query(Users).all()

    return data
