from fastapi import HTTPException,Depends
from passlib.context import CryptContext
from datetime import datetime,timezone,timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models import User
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

algorithm="HS256"
SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data:dict):
    data_copy = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    data_copy.update({'exp':expire})

    access_token = jwt.encode(data_copy,SECRET_KEY,algorithm=algorithm)

    return access_token


def decode_access_token(token: str):
    try:
        data = jwt.decode(token,SECRET_KEY,algorithms=[algorithm])
    except JWTError:
        raise HTTPException(status_code=403,detail="Could not validate credentials")

    if 'user_id' not in data:
        raise HTTPException(status_code=403,detail="Could not validate credentials")

    user_id = data["user_id"]

    return user_id

def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    user_id = decode_access_token(token)
    find_user = db.query(User).filter(User.id == user_id).first()
    if find_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return find_user