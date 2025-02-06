import uuid
from typing import List

from fastapi import APIRouter, HTTPException

from app_bookmanager.models.models import Author
from app_bookmanager.repositories.book_author_manager_repository import AuthorManagerRepository
from app_bookmanager.schemas.book_author_manager_schemas import AuthorCreate, AuthorResponse, BookResponse, \
    AuthorBooksResponse
from app_bookmanager.services.book_author_manager_services import AuthorManagerService
from db.database import SessionLocal

router = APIRouter(prefix="/authors", tags=["Authors"])

db = SessionLocal()
repository = AuthorManagerRepository(db)
service = AuthorManagerService(repository)

@router.post('/create-author')
def create_author(author: AuthorCreate):
    data = Author(name=author.name)
    service.create(data)
    return f'Successfully created author: {data.name}'

@router.get('/get-all-authors', response_model=List[AuthorResponse])
def get_authors():
    return service.get_all()

@router.get('/get-author', response_model=AuthorResponse)
def get_author_by_id(author_id: uuid.UUID):
    return service.get_by_id(author_id)

@router.post('/add-book-to-author')
def add_book_to_author(book_id: uuid.UUID, author_id: uuid.UUID):
    service.add_book_to_author(author_id=author_id, book_id=book_id)
    return f'Successfully added book to author: {book_id}'

@router.get('/get-books_written_author', response_model=AuthorBooksResponse)
def get_books_written_author(author_id: uuid.UUID):

    author = service.get_all_books_written_author_by_id(author_id)

    if author:
        return AuthorBooksResponse(authors_name=author.name,
                                   books=[BookResponse(title=book.title) for book in author.books])
    raise HTTPException(status_code = 404, detail="Author not found")


@router.delete('/delete-author')
def remove_author(author_id: uuid.UUID):
    service.delete(author_id)
    return f'Successfully deleted author!'