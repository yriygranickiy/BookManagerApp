import uuid
from pydantic import BaseModel


class EventSchema(BaseModel):
    id_book_instance: uuid.UUID
    username: str
    status: str
    timestamp: int

