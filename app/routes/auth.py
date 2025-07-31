from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.crud.user import get_user_by_username, create_user
from app.auth.jwt_handler import create_access_token
from app.utils.password import hash_password, verify_password
from app.database import get_session

router = APIRouter()

@router.post(path="/register")
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    if get_user_by_username(session, user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )

    return create_user(session, user)

@router.post(path="/login")
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    user = get_user_by_username(session, user_data.username)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"username": user.username, "user_id": user.id, "role": user.role})

    return {"access_token": token}
