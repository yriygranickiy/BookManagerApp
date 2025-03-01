import uuid

from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password: str


class RoleRequest(BaseModel):
    name: str

class RoleResponse(BaseModel):
    id: uuid.UUID
    name: str

class PermissionRequest(BaseModel):
    name: str

class PermissionResponse(BaseModel):
    id: uuid.UUID
    name: str

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    password: str
    roles: list[RoleResponse]





