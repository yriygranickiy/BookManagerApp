from sqlalchemy.orm import Session

from app_authorization.models.models import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(username == User.username).first()

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
