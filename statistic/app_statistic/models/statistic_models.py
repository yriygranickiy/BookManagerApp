import uuid

from sqlalchemy import Column, UUID, String, DateTime

from statistic.db.database import Base
class StatisticModel(Base):
    __tablename__ = 'statistics'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    book_instance_id = Column(UUID(as_uuid=True), nullable=False)
    username = Column(String, nullable=False)
    status = Column(String, nullable=False)
    time_updated = Column(DateTime, nullable=False)


