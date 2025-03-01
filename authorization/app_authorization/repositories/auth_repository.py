import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type

from sqlalchemy.orm import Session, DeclarativeMeta

from app_authorization.models.models import User, Roles, Permissions

T = TypeVar('T')


class ABCAuthorizationRepository(ABC, Generic[T]):

    @abstractmethod
    def get_by_name(self, name: str) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def create(self, model: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: uuid.UUID, user: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_link_model_to_model(self, model: Type[DeclarativeMeta], **fields) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: uuid.UUID) -> T:
        raise NotImplementedError


class BaseAuthorizationRepository(ABCAuthorizationRepository):

    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, model_id: uuid.UUID) -> T:
        return self.db.query(self.model).filter_by(id=model_id).first()

    def get_by_name(self, name: str) -> T:
        return self.db.query(self.model).filter_by(name=name).first()

    def create(self, model: T) -> None:
        self.db.add(model)
        self.db.commit()

    def update(self, model_id: uuid.UUID, updated_model: dict) -> None:
        model = self.db.query(self.model).filter_by(id=model_id).first()
        if not model:
            return None
        for k, v in updated_model.items():
            setattr(model, k, v)
        self.db.commit()
        self.db.refresh(model)

    def get_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def delete(self, model_id: uuid.UUID):
        model = self.db.query(self.model).filter_by(id=model_id).first()
        self.db.delete(model)
        self.db.commit()

    def add_link_model_to_model(self, model: Type[DeclarativeMeta], **fields) -> None:
        exists = self.db.query(model).filter_by(**fields).first()
        if not exists:
            data = model(**fields)
            self.db.add(data)
            self.db.commit()
        else:
            print(f'The relationship is already exists!')


class UserRepository(BaseAuthorizationRepository):

    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_name(self, username: str) -> User:
        return self.db.query(self.model).filter_by(username=username).first()
class RoleRepository(BaseAuthorizationRepository):

    def __init__(self, db: Session):
        super().__init__(db, Roles)


class PermissionRepository(BaseAuthorizationRepository):
    def __init__(self, db: Session):
        super().__init__(db, Permissions)
