import uuid

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class BookInstanceRequest(BaseModel):
    book_id: uuid.UUID
    status: str

