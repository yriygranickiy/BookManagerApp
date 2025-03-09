import uuid
from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status

from app_bookmanager.models.bookmanager_models import Publisher
from app_bookmanager.repositories.book_manager_repository import PublisherManagerRepository
from app_bookmanager.schemas.book_manager_schemas import PublisherRequest, PublisherResponse, BooksPublisherResponse, \
    BookResponse
from app_bookmanager.services.book_manager_services import PublisherManagerService
from db.database import SessionLocal

db = SessionLocal()
repository = PublisherManagerRepository(db)
service = PublisherManagerService(repository)

router = APIRouter(prefix="/publisher", tags=["Publisher"])


@router.post("/create-publisher", status_code=status.HTTP_201_CREATED)
def create_publisher(publisher_request: PublisherRequest):
    try:
        publisher = Publisher(title=publisher_request.title,
                              location=publisher_request.location)
        service.create(publisher)
        return f'Successfully created publisher'
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/update-publisher/{id_publisher}", status_code=status.HTTP_200_OK)
def update_publisher(id_publisher: uuid.UUID, updated_publisher: dict):
    publisher = service.get_by_id(id_publisher)
    if not publisher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Publisher with id: {id_publisher} not found")
    service.update(id_publisher, updated_publisher)
    return f'Successfully updated publisher'
@router.get("/publishers-list", status_code=status.HTTP_200_OK, response_model=List[PublisherResponse])
def get_publishers():
    try:
        return service.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{publisher_id}", status_code=status.HTTP_200_OK, response_model=PublisherResponse)
def get_publisher_by_id(publisher_id: uuid.UUID):
    publisher = service.get_by_id(publisher_id)
    if not publisher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Publisher with id: {publisher_id} not found')
    return publisher

@router.get("/get-books-by-publisher/{name_publisher}", status_code=status.HTTP_200_OK,
            response_model=BooksPublisherResponse)
def get_books_by_publisher_id(name_publisher: str):
    publisher = service.get_books_by_publisher(name_publisher)

    if publisher:
        return BooksPublisherResponse(publisher_title=name_publisher,
                                      books=[BookResponse(id=book.id,
                                                          title=book.title,
                                                          numbers_page=book.numbers_page) for book in publisher.books])
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Publisher with id: {name_publisher} not found')


@router.delete("/{publisher_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_publisher(publisher_id: uuid.UUID):
    publisher = service.get_by_id(publisher_id)
    if publisher:
        service.delete(publisher)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Publisher with id: {publisher_id} not found')
