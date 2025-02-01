from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from authorization.db.database import get_db
from authorization.app.repositories.user_repository import UserRepository
from authorization.app.schemas.user_schema import UserCreate
from authorization.app.services.auth_service import AuthService
from authorization.app.utils.security import create_access_token

router = APIRouter()
user_repo = UserRepository()
auth_service = AuthService(user_repo)


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    auth_service.register_user(db=db, user_data=user)
    return f'Successfully registered user!'

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = auth_service.authenticate(db=db, username=username, password=password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "role": user.role},
                                       expires_delta=timedelta(hours=1))
    return {"access_token": access_token, "token_type": "bearer"}
