import uuid

from sqlalchemy import Column, UUID, String

from db.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)