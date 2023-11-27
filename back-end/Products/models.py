from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime,Time,JSON,Date,Time
from sqlalchemy.sql import func

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    role = Column(String)
    is_active = Column(Boolean,default=True)


class Products(Base):
    __tablename__ ='products'

    id = Column(Integer,primary_key=True,index=True)
    actual_cost = Column(Integer)
    created_by = Column(String)
    created_on =Column(Date)
    discount = Column(JSON)
    end_date =Column(Date)
    end_time =Column(Time)
    location =Column(String)
    long_description =Column(String)
    manager=Column(String)
    name = Column(String)
    no_of_tests=Column(Integer)
    short_description = Column(String)
    start_date = Column(Date)
    start_time = Column(Time)
    type=Column(String)
    updated_by = Column(String)
    updated_on = Column(Date)
