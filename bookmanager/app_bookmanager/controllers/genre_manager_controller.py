import uuid
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status

from app_bookmanager.models.models import Genre
from app_bookmanager.repositories.book_manager_repository import GenreManagerRepository
from app_bookmanager.schemas.book_manager_schemas import GenreRequest, GenreResponse, BooksGenreResponse, BookResponse
from app_bookmanager.services.book_manager_services import GenreManagerService
from db.database import SessionLocal

router = APIRouter(prefix="/genre", tags=["Genre"])

db = SessionLocal()
repository = GenreManagerRepository(db)
service = GenreManagerService(repository)


@router.post("/create-genre", status_code=status.HTTP_201_CREATED)
def create_genre(genre: GenreRequest):
    try:
        genre_request = Genre(title=genre.title)
        service.create(genre_request)
    except Exception as e:
        return HTTPStatus.BAD_REQUEST, str(e)

@router.put("/update-genre/{id_genre}", status_code=status.HTTP_200_OK)
def update_genre(id_genre: uuid.UUID, updated_genre: dict):
    genre = service.get_by_id(id_genre)
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Genre with id: {id_genre} not found")
    service.update(id_genre, updated_genre)
    return f'Successfully updated genre'


@router.get("/all-genres", response_model=List[GenreResponse], status_code=status.HTTP_200_OK)
def get_genres():
    try:
        return service.get_all()
    except Exception as e:
        return HTTPStatus.BAD_REQUEST, str(e)


@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre_by_genre_id(genre_id: uuid.UUID):
    genre = service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Genre with id: {genre_id}  not found')
    return genre


@router.get("/books-by-genre/{title}", response_model=BooksGenreResponse, status_code=status.HTTP_200_OK)
def get_books_by_genre_title(title: str):

    genre = service.get_books_by_genre(title)

    if genre:
        return BooksGenreResponse(genre_title=genre.title,
                                  books=[BookResponse(id=book.id,
                                                      title=book.title,
                                                      numbers_page=book.numbers_page) for book in genre.books])
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Genre with title: {title} not found')


@router.delete("/{genre_id}", response_model=GenreResponse)
def remove_genre_by_genre_id(genre_id: uuid.UUID):
    genre = service.get_by_id(genre_id)
    if genre:
        service.delete(genre_id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Genre with id: {genre_id}  not found')
