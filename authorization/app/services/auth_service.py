from sqlalchemy.orm import Session

from authorization.app.models.models import User
from authorization.app.repositories.user_repository import UserRepository
from authorization.app.schemas.user_schema import UserCreate
from authorization.app.utils.security import verify_password, get_password_hash


class AuthService:
    def __init__(self,user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, db: Session, username: str, password: str) -> User:
        user = self.user_repo.get_user_by_username(db=db, username=username)
        if not user or not verify_password(password, user.password):
            return None
        return user

    def register_user(self, db: Session, user_data: UserCreate):
        hashed_password = get_password_hash(user_data.password)
        user = self.user_repo.create_user(db=db, user=User(
                                                  username=user_data.username,
                                                  password=hashed_password,
                                                  role=user_data.role))
        return user

