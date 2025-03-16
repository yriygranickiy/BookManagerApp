import uuid

from pydantic import BaseModel

class BookRequest(BaseModel):
    title: str
    pages: int

class BookInstanceRequest(BaseModel):
    book_id: uuid.UUID
    status: str

class GenreToBookRequest(BaseModel):
    book_id: uuid.UUID
    genre_id: uuid.UUID

class PublisherToBookRequest(BaseModel):
    book_id: uuid.UUID
    publisher_id: uuid.UUID

class AuthorBookRequest(BaseModel):
    book_id: uuid.UUID
    author_id: uuid.UUID

class GenreRequest(BaseModel):
    title: str

class PublisherRequest(BaseModel):
    title: str
    location:str

class AuthorRequest(BaseModel):
    first_name: str
    last_name: str
    surname: str
