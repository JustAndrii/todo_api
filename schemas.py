from datetime import datetime
from pydantic import BaseModel,ConfigDict



class UserCreate(BaseModel):

    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created: datetime
    model_config  = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):

    title: str
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    completed: bool
    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class LoginResponse(BaseModel):
    id:int
    email: str
    created: datetime
