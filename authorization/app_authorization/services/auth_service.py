from sqlalchemy.orm import Session

from app_authorization.models.models import User
from app_authorization.repositories.user_repository import UserRepository
from app_authorization.schemas.user_schema import UserCreate
from app_authorization.utils.security import verify_password, get_password_hash


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, username: str, password: str) -> User:
        user = self.user_repo.get_user_by_username(username=username)
        if not user or not verify_password(password, user.password):
            return None
        return user

    def register_user(self, user_data: UserCreate):
        existing_user = self.user_repo.get_user_by_username(username=user_data.username)
        if existing_user:
            return None
        hashed_password = get_password_hash(user_data.password)
        return self.user_repo.create_user(user=User(username=user_data.username,
                                             password=hashed_password,
                                             role='reader'))
