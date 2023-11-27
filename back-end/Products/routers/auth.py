from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import timedelta,datetime


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY ='3f9fb5535bda2e553b429d20f07ce3c0f68314b14bd9780fc4ff4aa6d2ba70d4'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

db_dependancy = Annotated[Session,Depends(get_db)]
form_dependancy = Annotated[OAuth2PasswordRequestForm,Depends()]
user_dependancy = Annotated[str,Depends(oauth2_bearer)]

class CreateUserRequest(BaseModel):
    email:str
    username:str
    first_name:str
    last_name:str
    password:str
    role:str

class Token(BaseModel):
    access_token:str
    token_type:str

class LoginRequest(BaseModel):
    username:str
    password:str


def authenticate_user(username:str ,password:str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:int,role:str,expires_delta:timedelta):

    encode = {'sub':username,'id':user_id,'role':role}
    expires = datetime.utcnow() + (expires_delta)
    encode.update({'exp':expires})

    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(token:user_dependancy):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        user_role:str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')

        return {'username':username,'user_id':user_id,'user_role':user_role}

    except JWTError:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')




@router.post("/",status_code =status.HTTP_201_CREATED)
def create_user(db:db_dependancy,create_user_request:CreateUserRequest):

    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password =bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True
    )

    db.add(create_user_model)
    db.commit()

    return {"message": "user created successfully", "status": status.HTTP_201_CREATED}


@router.post('/authenticate')
def authenticate_login_user(loginDetails:LoginRequest,db:db_dependancy):
    user = db.query(Users).filter(Users.username == loginDetails.username).first()
    if not user:
        return False
    if not bcrypt_context.verify(loginDetails.password,user.hashed_password):
        return False
    return True

@router.post("/token",response_model=Token)
def login_for_access_token(form_data:form_dependancy,db:db_dependancy):

    user = authenticate_user(form_data.username,form_data.password,db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')

    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))

    return {'access_token':token,'token_type':'Bearer'}
