# from sqlalchemy.orm import Session
# from fastapi import APIRouter,Depends,HTTPException,Path
# from typing import Annotated
# from models import Todos
# from database import SessionLocal
# import models
# from starlette import status
# from pydantic import BaseModel,Field
# from .auth import get_current_user

# router = APIRouter(
#     prefix = '/admin',
#     tags=['admin']
# )

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependancy = Annotated[Session,Depends(get_db)]
# user_dependancy = Annotated[dict,Depends(get_current_user)]

# @router.get("/todos",status_code=status.HTTP_200_OK)
# def read_all_todos(user:user_dependancy,db:db_dependancy):

#     if user is None or user.get('user_role') != 'admin':
#         raise HTTPException(status_code=401,detail='Authentication failed')

#     data = db.query(Todos).all()
    
#     return {"message": "successful", "data": data, "status": status.HTTP_200_OK}

# @router.delete("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_todo(user:user_dependancy,db:db_dependancy,todo_id:int):

#     if user is None or user.get('user_role') != 'admin':
#         raise HTTPException(status_code=401,detail='Authentication failed')

#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if  todo_model is None:
#         raise HTTPException(status_code=401,detail='Item not found')

#     db.query(Todos).filter(Todos.id == todo_id).delete()
#     db.commit()

#     return {"message": "todo deleted successfully",  "status": status.HTTP_204_NO_CONTENT}
