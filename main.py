from fastapi import FastAPI
from database import Base, engine
from routers import users,tasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=False
)

Base.metadata.create_all(engine)

app.include_router(users.router)

app.include_router(tasks.router)
