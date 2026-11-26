from fastapi import FastAPI
from routers.tasks import router
from database import Base, engine
from models import Task

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def read_root():

    return {"message": "Hi! I am your task tracker. Keep doing your work everyday and achieve your goals!"}

app.include_router(router)