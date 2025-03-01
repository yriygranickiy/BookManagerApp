import uuid

from pydantic import BaseModel


class BookRequest(BaseModel):
    title: str
    numbers_page: int

class BookResponse(BaseModel):
    id: uuid.UUID
    title: str
    numbers_page: int
class BookInstanceRequest(BaseModel):
    book_id: uuid.UUID
    status: str

class BookInstanceResponse(BaseModel):
    id: uuid.UUID
    status: str

class AuthorRequest(BaseModel):
    first_name: str
    last_name: str
    surname: str

class AuthorResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    surname: str

class GenreRequest(BaseModel):
    title: str

class GenreResponse(BaseModel):
    id: uuid.UUID
    title: str

class PublisherRequest(BaseModel):
    title: str
    location: str

class PublisherResponse(BaseModel):
    id: uuid.UUID
    title: str
    location: str


class AuthorBooksResponse(BaseModel):
    authors_name: str
    books: list[BookResponse]

class BookAuthorResponse(BaseModel):
    book_title: str
    authors_name: list[AuthorResponse]

class GenresBookResponse(BaseModel):
    title_book: str
    genres: list[GenreResponse]

class BooksGenreResponse(BaseModel):
    genre_title: str
    books: list[BookResponse]

class BooksPublisherResponse(BaseModel):
    publisher_title: str
    books: list[BookResponse]


