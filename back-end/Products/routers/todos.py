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
#     prefix='/todos',
#     tags=['todos']
# )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependancy = Annotated[Session,Depends(get_db)]
# user_dependancy = Annotated[dict,Depends(get_current_user)]


# class TodoRequest(BaseModel):
#     title : str = Field(min_length=3)
#     description : str = Field(min_length=3,max_length=100)
#     priority:int = Field(lt=6)
#     complete :bool


# @router.get('/',status_code=status.HTTP_200_OK)
# def read_all_todos_of_one_user(user:user_dependancy,db:db_dependancy):

#     if  user is None:
#         raise HTTPException(status_code=401,detail='Authentication is failed') 

#     data = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()

#     return {'message':'sucessful','data':data,'status':status.HTTP_200_OK}

# @router.get('/{todo_id}',status_code=status.HTTP_200_OK)
# def read_todo_by_id(user:user_dependancy,db:db_dependancy,todo_id:int=Path(gt=0)):

#     if  user is None:
#         raise HTTPException(status_code=401,detail='Authentication is failed')

#     todos_list = db.query(Todos).filter(Todos.id == todo_id)\
#         .filter(Todos.owner_id == user.get('user_id')).first()

#     if todos_list is not None:
#         return {"message": "successful", "data": todos_list, "status": status.HTTP_200_OK}

#     raise HTTPException(status_code=404,detail="Item not found")

# @router.post('/',status_code=status.HTTP_201_CREATED)
# def create_todo(user:user_dependancy,db:db_dependancy,new_todo:TodoRequest):

#     if  user is None:
#         raise HTTPException(status_code=401,detail='Authentication is failed')

#     todo_model = Todos(**new_todo.dict(),owner_id=user.get('user_id'))

#     db.add(todo_model)
#     db.commit()

#     return {"message": "todo added successfully", "status": status.HTTP_201_CREATED}

# @router.put('/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
# def update_todo(user:user_dependancy,db:db_dependancy,
#                 updated_todo:TodoRequest,
#                 todo_id:int = Path(gt=0)):
#     if  user is None:
#         raise HTTPException(status_code=401,detail='Authentication is failed')

#     todo_model = db.query(Todos).filter(Todos.id == todo_id)\
#         .filter(Todos.owner_id == user.get('user_id')).first()

#     if todo_model is None:
#         raise HTTPException(status_code=404,detail="Item not found")

#     todo_model.title = updated_todo.title
#     todo_model.description = updated_todo.description
#     todo_model.priority = updated_todo.priority
#     todo_model.complete = updated_todo.complete

#     db.add(todo_model)
#     db.commit()

#     return {"message": "todo updated successfully", "status": status.HTTP_204_NO_CONTENT}

# @router.delete('/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
# def delete_todo(user:user_dependancy,db:db_dependancy,todo_id:int = Path(gt=0)):

#     if  user is None:
#         raise HTTPException(status_code=401,detail='Authentication is failed')

#     todo_model = db.query(Todos).filter(Todos.id == todo_id)\
#         .filter(Todos.owner_id == user.get('user_id')).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404,detail="Item not found")

#     db.query(Todos).filter(Todos.id == todo_id).delete()
#     db.commit()
#     return {"message": "todo deleted successfully", "status": status.HTTP_204_NO_CONTENT}
