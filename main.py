from fastapi import FastAPI
from database import Base, engine
from routers import users,tasks

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(users.router)  # app, включи в себе endpoints, які лежать у users.router

app.include_router(tasks.router)