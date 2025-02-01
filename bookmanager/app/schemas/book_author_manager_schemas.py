import uuid
from typing import List

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str


class BookResponse(BaseModel):
    # id: uuid.UUID
    title: str


class AuthorCreate(BaseModel):
    name: str


class AuthorResponse(BaseModel):
    # id: uuid.UUID
    name: str

    class Config:
        orm_mode = True


class AuthorBooksResponse(BaseModel):
    authors_name: str
    books: list[BookResponse]


class BookAuthorResponse(BaseModel):
    book_title: str
    authors_name: list[AuthorResponse]


