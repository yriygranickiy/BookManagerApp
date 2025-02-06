import uuid

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str