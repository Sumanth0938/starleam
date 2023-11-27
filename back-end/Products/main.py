from fastapi import FastAPI
from database import engine,SessionLocal
from routers import auth , todos, admin , users ,products
from fastapi.middleware.cors import CORSMiddleware

import models

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(products.router)
