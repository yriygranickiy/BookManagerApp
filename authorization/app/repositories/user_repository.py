from sqlalchemy.orm import Session

from authorization.app.models.models import User


class UserRepository:
    def get_user_by_username(self, db: Session, username: str) -> User:
        return db.query(User).filter(username == User.username).first()

    def create_user(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
