from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app_authorization.repositories.user_repository import UserRepository
from app_authorization.schemas.user_schema import UserCreate
from app_authorization.services.auth_service import AuthService
from app_authorization.utils.security import create_access_token
from db.database import SessionLocal

router = APIRouter()
db = SessionLocal()
user_repo = UserRepository(db)
auth_service = AuthService(user_repo)


@router.post("/register")
def register(user: UserCreate):
    new_user = auth_service.register_user(user_data=user)
    if not new_user:
        raise HTTPException(status_code=401, detail="User already exists")
    return new_user


@router.post("/login")
def login(username: str, password: str):
    user = auth_service.authenticate(username=username, password=password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "role": user.role},
                                       expires_delta=timedelta(hours=1))
    return {"access_token": access_token, "token_type": "bearer"}
