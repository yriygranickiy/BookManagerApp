import uuid
from pydantic import BaseModel


class EventSchema(BaseModel):
    id: uuid.UUID
    username: str
    id_book_instance: uuid.UUID
    status: str

