import uuid
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from starlette import status

from app_bookmanager.repositories.book_manager_repository import BookInstanceRepository
from app_bookmanager.schemas.book_manager_schemas import BookInstanceRequest, BookInstanceResponse
from app_bookmanager.models.bookmanager_models import BookInstance
from app_bookmanager.services.book_manager_services import BookInstanceService
from db.database import SessionLocal

router = APIRouter(prefix="/book_instance", tags=["BookInstance"])

db = SessionLocal()
repository = BookInstanceRepository(db)
service = BookInstanceService(repository)


@router.post("/crate-book-instance", status_code=status.HTTP_201_CREATED)
def create_book_instance(request: BookInstanceRequest):
    try:
        book_instance = BookInstance(book_id=request.book_id,
                                     status=request.status)
        service.create(book_instance)
        return f'Successfully registered book_instance!'
    except Exception as e:
        return HTTPStatus.BAD_REQUEST, str(e)

@router.put("/update-book-instance/{book_instance_id}", status_code=status.HTTP_200_OK)
def update_book_instance(book_instance_id: uuid.UUID, updated_data: dict):
    book_instance = service.get_by_id(book_instance_id)
    if book_instance is None:
        return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"BookInstance with id: {book_instance_id} not "
                                                                      f"found")
    service.update(book_instance_id, updated_data)
    return f'Successfully registered book_instance!'

@router.get("/book-instances", response_model=list[BookInstanceResponse], status_code=status.HTTP_200_OK)
def get_all_book_instance():
    return service.get_all()

@router.get("/book-instance/{book_id}", response_model= BookInstanceResponse, status_code=status.HTTP_200_OK)
def get_book_instance_by_id(book_instance_id: uuid.UUID):
    book_instance = service.get_by_id(book_instance_id)
    if not book_instance:
        raise HTTPException(status_code=404, detail=f'BookInstance with: {book_instance_id} not found ')
    return book_instance

@router.delete("/book-instance/{book_instance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_instance_by_id(book_instance_id: uuid.UUID):
    book_instance = service.get_by_id(book_instance_id)
    if book_instance:
        service.delete(book_instance_id)
    else:
        raise HTTPException(status_code=404, detail=f'BookInstance does not exist')

