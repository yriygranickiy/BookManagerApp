import json
import uuid

from fastapi import APIRouter, HTTPException
from kafka import KafkaProducer
from starlette import status

from app_bookmanager.models.bookmanager_models import Book
from app_bookmanager.repositories.book_manager_repository import BookManagerRepository

from app_bookmanager.schemas.book_manager_schemas import BookResponse, AuthorResponse, \
    BookAuthorResponse, BookRequest
from app_bookmanager.services.book_manager_services import BookManagerService
from db.database import SessionLocal

router = APIRouter(prefix="/book", tags=["Books"])
db = SessionLocal()
repository = BookManagerRepository(db)
service = BookManagerService(repository)

@router.post('/create-book', status_code=status.HTTP_201_CREATED)
def create_book(book_response: BookRequest):
    book = Book(
        title=book_response.title,
        numbers_page=book_response.numbers_page
    )
    service.create(book)
    return f'Successfully registered book!'


@router.post('/add-genre-to-book', status_code=status.HTTP_201_CREATED)
def add_book_to_genre(book_id: uuid.UUID, genre_id: uuid.UUID):
    service.add_book_to_genre(book_id=book_id, genre_id=genre_id)
    return f'Successfully added genre to book!'

@router.post('/add-book-to-publisher', status_code=status.HTTP_201_CREATED)
def add_book_to_publisher(book_id: uuid.UUID, publisher_id: uuid.UUID):
    service.add_book_to_publisher(book_id=book_id, publisher_id=publisher_id)
    return f'Successfully added publisher to book!'

@router.post('/add-author-to-book')
def add_author_to_book(book_id: uuid.UUID, author_id: uuid.UUID):
    service.add_author_to_book(book_id=book_id, author_id=author_id)
    return f'Successfully added author to book!'

@router.put('/update-book/{book_id}', status_code=status.HTTP_200_OK)
def update_book(book_id: uuid.UUID, updated_data: dict):
    book = service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with id: {book_id} not found')
    service.update(book_id, updated_data)
    return f'Successfully updated book!'


@router.get('/get-book/{book_id}', response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: uuid.UUID):
    book = service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with id : {book_id}  not found')
    return service.get_by_id(book_id)

@router.get('/get-books', response_model=list[BookResponse], status_code=status.HTTP_200_OK)
def get_all_books():

    return service.get_all()

@router.get('/get-authors-from-book/{book_title}', response_model=BookAuthorResponse)
def get_all_authors_from_book_by_title(book_title: str):
    books = service.get_all_authors_from_book_by_title(book_title)
    if books:
        return BookAuthorResponse(book_title=books.title,
                                  authors_name=[AuthorResponse(id=author.id,
                                                               last_name=author.last_name,
                                                               first_name=author.first_name,
                                                               surname=author.surname) for author in books.authors])
    raise HTTPException(status_code=404, detail=f'Book with title: {book_title} not found')

@router.delete('/remove-book/{id}')
def remove_book(book_id: uuid.UUID):
    book = service.get_by_id(book_id)
    if book:
        service.delete(book_id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with id: {book_id}  not found')
