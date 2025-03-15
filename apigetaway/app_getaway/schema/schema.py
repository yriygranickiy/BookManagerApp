import uuid

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str

class BookInstanceRequest(BaseModel):
    book_id: uuid.UUID
    status: str

