import json
import os
import uuid
from _pydatetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, HTTPException,Request
from kafka import KafkaProducer
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
#
KAFKA_SERVER = os.getenv("KAFKA_BROKER_URL", "localhost:29092")
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'user_actions')
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_message_to_kafka(username: str, id: uuid.UUID, status: str, time: datetime):
    message = {
        "id": str(id),
        "username": username,
        "status": status,
        "time": int(time)
    }
    producer.send(KAFKA_TOPIC, message)

@router.post("/create-book-instance", status_code=status.HTTP_201_CREATED)
def create_book_instance(request: BookInstanceRequest):
    try:
        book_instance = BookInstance(book_id=request.book_id,
                                     status=request.status)
        service.create(book_instance)
        return f'Successfully registered book_instance!'
    except Exception as e:
        return HTTPStatus.BAD_REQUEST, str(e)

@router.put("/update-book-instance/{book_instance_id}", status_code=status.HTTP_200_OK)
def update_book_instance(book_instance_id: uuid.UUID, updated_data: dict, request: Request):
    book_instance = service.get_by_id(book_instance_id)
    if book_instance is None:
        return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"BookInstance with id: {book_instance_id} not "
                                                                      f"found")
    timestamp = datetime.timestamp(datetime.now())
    service.update(book_instance_id, updated_data)
    send_message_to_kafka(request.headers.get('username'),book_instance_id, updated_data.get("status"), timestamp)

    return f'Successfully updated book instance!'

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

