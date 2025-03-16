import uuid
from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status

from app_bookmanager.models.bookmanager_models import Author
from app_bookmanager.repositories.book_manager_repository import AuthorManagerRepository
from app_bookmanager.schemas.book_manager_schemas import AuthorResponse, BookResponse, \
    AuthorBooksResponse, AuthorRequest
from app_bookmanager.services.book_manager_services import AuthorManagerService
from db.database import SessionLocal

router = APIRouter(prefix="/authors", tags=["Authors"])

db = SessionLocal()
repository = AuthorManagerRepository(db)
service = AuthorManagerService(repository)

@router.post('/create-author', status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorRequest):
    data = Author(first_name=author.first_name, last_name=author.last_name, surname=author.surname,)
    service.create(data)
    return f'Successfully created author!'

@router.post('/add-book-to-author', status_code=status.HTTP_201_CREATED)
def add_book_to_author(book_id: uuid.UUID, author_id: uuid.UUID):
    service.add_book_to_author(author_id=author_id, book_id=book_id)
    return f'Successfully added book to author: {book_id}'

@router.put('/update-author/{author_id}', status_code=status.HTTP_200_OK)
def update_author(author_id: uuid.UUID, updated_data: dict):
    author = service.get_by_id(author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Author with id: {author_id} not found')
    service.update(author_id, updated_data)
    return f'Successfully updated author!'

@router.get('/get-books-written-author/{author_last_name}', response_model=AuthorBooksResponse,status_code=status.HTTP_200_OK)
def get_books_written_author(author_last_name: str):

    author = service.get_all_books_written_author_by_last_name(author_last_name)

    if author:
        return AuthorBooksResponse(authors_name=author.last_name,
                                   books=[BookResponse(title=book.title,
                                                       id=book.id,
                                                       numbers_page=book.numbers_page) for book in author.books])
    raise HTTPException(status_code = 404, detail="Author not found")
@router.get('/get-all-authors', response_model=List[AuthorResponse], status_code=status.HTTP_200_OK)
def get_authors():
    return service.get_all()

@router.get('/get-author/{author_id}', response_model=AuthorResponse, status_code=status.HTTP_200_OK)
def get_author_by_id(author_id: uuid.UUID):
    author = service.get_by_id(author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return author

@router.delete('/delete-author',status_code=status.HTTP_204_NO_CONTENT)
def remove_author(author_id: uuid.UUID):
    author = service.get_by_id(author_id)
    if author:
        service.delete(author_id)
    else:
        raise HTTPException(status_code=404, detail=f"Author is not found with id: {author_id}")
    return None