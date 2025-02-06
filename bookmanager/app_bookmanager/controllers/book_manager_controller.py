import uuid

from fastapi import APIRouter, HTTPException

from app_bookmanager.models.models import Book
from app_bookmanager.repositories.book_author_manager_repository import BookManagerRepository

from app_bookmanager.schemas.book_author_manager_schemas import BookCreate, BookResponse, AuthorResponse, \
    BookAuthorResponse
from app_bookmanager.services.book_author_manager_services import BookManagerService
from db.database import SessionLocal

router = APIRouter(prefix="/book", tags=["Books"])
db = SessionLocal()
repository = BookManagerRepository(db)
service = BookManagerService(repository)


@router.post('/create-book')
def create_book(book: BookCreate):
    data = Book(title=book.title)
    service.create(data)
    return f'Successfully registered book!'


@router.get('/get-book', response_model=BookResponse)
def get_book_by_id(book_id: uuid.UUID):
    return service.get_by_id(book_id)


@router.get('/get-books', response_model=list[BookResponse])
def get_all_books():
    return service.get_all()


@router.post('/add-author-to-book')
def add_author_to_book(book_id: uuid.UUID, author_id: uuid.UUID):
    service.add_author_to_book(book_id=book_id, author_id=author_id)
    return f'Successfully added author to book!'


@router.get('/get-authors-from-book', response_model=BookAuthorResponse)
def get_all_authors_from_book_by_title(book_title: str):
    books = service.get_all_authors_from_book_by_title(book_title)
    if books:
        return BookAuthorResponse(book_title=books.title,
                                  authors_name=[AuthorResponse(name=author.name) for author in books.authors])
    raise HTTPException(status_code=404, detail='Book not found')

@router.delete('/remove-author-from-book')
def remove_book(book_id: uuid.UUID):
    service.delete(book_id)
    return f'Successfully removed book!'
