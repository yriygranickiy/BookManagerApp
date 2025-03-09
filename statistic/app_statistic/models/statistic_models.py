import uuid

from sqlalchemy import Column, UUID, String

from statistic.db.database import Base
class StatisticModel(Base):
    __tablename__ = 'statistics'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name_user = Column(String, nullable=False)
    book_instance_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    status = Column(String, nullable=False)


