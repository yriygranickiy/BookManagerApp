import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from fastapi import HTTPException
from starlette import status

from app_authorization.models.models import User, RolePermission, UserRoles
from app_authorization.repositories.auth_repository import UserRepository, ABCAuthorizationRepository, RoleRepository, \
    PermissionRepository
from app_authorization.schemas.user_schema import UserRequest
from app_authorization.utils.security import verify_password, get_password_hash, get_data_user_from_token

T = TypeVar('T')


class ABCAuthService(ABC, Generic[T]):

    @abstractmethod
    def create(self, model: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, model_id: uuid.UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def update(self, model_id: uuid.UUID, data: T):
        raise NotImplementedError

    @abstractmethod
    def delete(self, model_id: uuid.UUID) -> T:
        raise NotImplementedError


class AuthorizationService(ABCAuthService):
    def __init__(self, repository: ABCAuthorizationRepository):
        self.repository = repository

    def create(self, model: T) -> None:
        return self.repository.create(model)

    def get_by_id(self, model_id: uuid.UUID) -> T:
        return self.repository.get_by_id(model_id)

    def get_all(self) -> list[T]:
        return self.repository.get_all()

    def update(self, model_id: uuid.UUID, data: T):
        self.repository.update(model_id, data)

    def delete(self, model_id: uuid.UUID):
        self.repository.delete(model_id)


class UserService(AuthorizationService):
    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository):
        super().__init__(user_repository)
        self.user_repository = user_repository
        self.role_repository = role_repository

    def authenticate(self, user_request: UserRequest) -> User:
        user = self.user_repository.get_by_name(user_request.username)
        if not user or not verify_password(user_request.password, user.password):
            return None
        return user

    def register_user(self, user_data: UserRequest):
        existing_user = self.repository.get_by_name(user_data.username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User already exists')
        hashed_password = get_password_hash(user_data.password)
        role = self.role_repository.get_by_name('READER')
        user = User(username=user_data.username, password=hashed_password)
        user.roles.append(role)
        self.user_repository.create(user)
        return user


class RoleService(AuthorizationService):
    def __init__(self, role_repository: RoleRepository):
        super().__init__(role_repository)
        self.role_repository = role_repository

    def add_role_to_user(self, user_id: uuid.UUID, role_id: uuid.UUID):
        self.role_repository.add_link_model_to_model(UserRoles,user_id=user_id, role_id=role_id)


class PermissionService(AuthorizationService):
    def __init__(self, permission_repository: PermissionRepository):
        super().__init__(permission_repository)
        self.permission_repository = permission_repository

    def add_permission_to_role(self, role_id: uuid.UUID, permission_id: uuid.UUID):
        self.permission_repository.add_link_model_to_model(RolePermission, role_id=role_id, permission_id=permission_id)

