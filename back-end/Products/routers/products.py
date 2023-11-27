from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,Path
from typing import Annotated
from database import SessionLocal
import models
from starlette import status
from pydantic import BaseModel,Field
from .auth import get_current_user
from models import Products
from datetime import date, time
from starlette.responses import JSONResponse

router = APIRouter(
    prefix = '/products',
    tags=['products']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session,Depends(get_db)]
user_dependancy = Annotated[dict,Depends(get_current_user)]


class DiscountRequest(BaseModel):
    amount : int = Field(gt=0)
    cost : str
    dead_line : str

class ProductRequest(BaseModel):
     actual_cost : int = Field(gt=0)
     created_by : str
     created_on : date
     discount : DiscountRequest | None = None
     end_date : date
     end_time : time
     location : str
     long_description : str
     manager : str
     name : str
     no_of_tests : int = Field(gt=0)
     short_description : str
     start_date : date
     start_time : time
     type : str
     updated_by :str
     updated_on : date

@router.post('/add_new_product',status_code=status.HTTP_201_CREATED)
async def add_new_product(user:user_dependancy,db:db_dependancy,new_product:ProductRequest):

    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401,detail='Authentication failed')

    discount_data = dict(new_product.discount) if new_product.discount else None

    product_model = Products(
        
        actual_cost = new_product.actual_cost,
        created_by = new_product.created_by,
        created_on = new_product.created_on,
        discount = discount_data,
        end_date = new_product.end_date,
        end_time = new_product.end_time,
        location = new_product.location,
        long_description = new_product.long_description,
        manager = new_product.manager,
        name = new_product.name,
        no_of_tests = new_product.no_of_tests,
        short_description = new_product.short_description,
        start_date = new_product.start_date,
        start_time = new_product.start_time,
        type = new_product.type,
        updated_by = new_product.updated_by,
        updated_on = new_product.updated_on,
        
    )

    db.add(product_model)
    db.commit()

    return {"message" : "product added successfully",
            "status_code":status.HTTP_201_CREATED}

@router.get('/get_all_products',status_code=status.HTTP_200_OK)
def get_all_products(db:db_dependancy):

    try:
        product_model = db.query(Products).all()

        return {"message":"successfull","data":product_model,"status":status.HTTP_200_OK}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.get('/search_by_id/{product_id}',status_code=status.HTTP_200_OK)
def get_product_by_id(db:db_dependancy,product_id:int = Path(gt=0)):

    try:
        product_model = db.query(Products)\
                        .filter(Products.id == product_id).first()

        if product_model is None:
            return JSONResponse({"detail": "NO_PRODUCTS_FOUND"}, status_code=404)
        
        return {"message":"successfull","data":product_model,"status":status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.get('/search_by_location/{product_location}',status_code=status.HTTP_200_OK)
def get_product_by_location(db:db_dependancy,product_location:str=Path):

    try:
        product_model = db.query(Products).filter(Products.location == product_location).all()

        if not  product_model :
            return JSONResponse({"detail": "NO_PRODUCTS_FOUND"}, status_code=404)
        
        return {"message":"successfull","data":product_model,"status":status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.get('/search_by_created_date/{product_created_date}',status_code=status.HTTP_200_OK)
def get_product_by_created_date(db:db_dependancy,product_created_date:date):

    try:
        product_model = db.query(Products).filter(Products.created_on == product_created_date).all()

        if not product_model :
            return JSONResponse({"detail": "NO_PRODUCTS_FOUND"}, status_code=404)
        
        return {"message":"successfull","data":product_model,"status":status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


@router.put('/update_product/{product_id}')
def update_product(user:user_dependancy,db:db_dependancy,update_product:ProductRequest,product_id:int =Path):

    try:    
        if user is None or user.get('user_role') != 'admin':
            raise HTTPException(status_code=401,detail='Authentication failed')
        
        product_model = db.query(Products).filter(Products.id == product_id).first()

        if not product_model :
            return JSONResponse({"detail": "PRODUCT_NOT_FOUND"}, status_code=404)

        discount_data = dict(update_product.discount) if update_product.discount else None

        product_model.actual_cost = update_product.actual_cost
        product_model.created_by = update_product.created_by 
        product_model.created_on = update_product.created_on
        product_model.discount = discount_data
        product_model.end_date = update_product.end_date
        product_model.end_time =  update_product.end_time
        product_model.location = update_product.location
        product_model.long_description  = update_product.long_description
        product_model.manager = update_product.manager 
        product_model.manager =  update_product.manager
        product_model.name  = update_product.name
        product_model.no_of_tests  = update_product.no_of_tests 
        product_model.short_description =  update_product.short_description
        product_model.start_date  = update_product.start_date
        product_model.start_time = update_product.start_time
        product_model.type  = update_product.type 
        product_model.updated_by  = update_product.updated_by
        product_model.updated_on = update_product.updated_on

        db.add(product_model)
        db.commit()

        return {"message": "product updated successfully", "status": status.HTTP_204_NO_CONTENT}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


@router.delete('/delete/{product_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db:db_dependancy,user:user_dependancy,product_id:int = Path(gt=0)):

    try:
        if  user is None:
            raise HTTPException(status_code=401,detail='Authentication is failed')

        product_model = db.query(Products).filter(Products.id == product_id).first()

        if product_model is None:
           return JSONResponse({"detail": " PRODUCT_NOT_FOUND"}, status_code=404)

        db.query(Products).filter(Products.id == product_id).delete()
        db.commit()

        return {"message": "todo deleted successfully", "status": status.HTTP_204_NO_CONTENT}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))