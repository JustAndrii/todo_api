from fastapi import APIRouter, Depends, HTTPException
from auth import hash_password

from models import User
from schemas import UserCreate, UserResponse,LoginResponse
from database import get_db
from auth import verify_password,create_access_token
from auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()



@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db = Depends(get_db)):
    find_user = db.query(User).filter(User.email == user.email).first()
    if find_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(email = user.email, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login')
def identify_person(login: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    find_user = db.query(User).filter(User.email == login.username).first()
    if find_user is None:
        raise HTTPException(status_code=400, detail="Email doesn't exist")
    if verify_password(login.password, find_user.hashed_password) is False:
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token({ 'user_id': find_user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me',response_model=LoginResponse)
def me(current_user = Depends(get_current_user)):
    return current_user



