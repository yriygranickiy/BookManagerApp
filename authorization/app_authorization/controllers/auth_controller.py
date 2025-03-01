import uuid
from datetime import timedelta

from fastapi import APIRouter, HTTPException
from starlette import status

from app_authorization.repositories.auth_repository import UserRepository, RoleRepository
from app_authorization.schemas.user_schema import UserRequest, UserResponse
from app_authorization.services.auth_service import UserService
from app_authorization.utils.security import create_access_token, get_data_user_from_token
from db.database import SessionLocal

router = APIRouter()
db = SessionLocal()
user_repo = UserRepository(db)
role_repo = RoleRepository(db)
auth_service = UserService(user_repo, role_repo)


@router.post("/register")
def register(user: UserRequest):
    new_user = auth_service.register_user(user_data=user)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return f'Successfully registered user!'


@router.post("/login")
def login(user_request: UserRequest):
    user = auth_service.authenticate(user_request=user_request)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    permissions = []
    for role in user.roles:
        permissions.extend([permission.name for permission in role.permissions])
    permissions = list(set(permissions))
    access_token = create_access_token(data={"username": user.username, "permissions": permissions},
                                       expires_delta=timedelta(hours=1))
    user_data = get_data_user_from_token(access_token)
    return {"access_token": access_token, "permissions": user_data["permissions"]}

@router.get("/get-all-users", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
def get_all_users():
    return auth_service.get_all()

@router.put("/update-user", status_code=status.HTTP_200_OK)
def update_user(id_user: uuid.UUID, data:dict):
    user = auth_service.get_by_id(id_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id_user} not found")
    auth_service.update(id_user, data)
    return f'Successfully updated user!'






