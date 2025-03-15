import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from sqlalchemy.orm import Session

from app_statistic.models.statistic_models import StatisticModel

T = TypeVar('T')


class ABCStatisticsManagerRepository(ABC, Generic[T]):

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def create(self, model: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: uuid.UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, model_id: uuid.UUID, updated_model: dict):
        raise NotImplementedError


class BaseStatisticsRepository(ABCStatisticsManagerRepository):

    def __init__(self, db: Session, model: T):
        self.db = db
        self.model = model

    def get_by_id(self, model_id: uuid.UUID) -> T:
        return self.db.query(self.model).filter_by(id=model_id).first()

    def create(self, model: T) -> None:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

    def get_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def delete(self, model_id: uuid.UUID) -> None:
        self.db.query(self.model).filter_by(id=model_id).delete()

    def update(self, model_id: uuid.UUID, updated_model: dict):
        model = self.db.query(self.model).filter_by(id=model_id).first()
        if not model:
            return None
        for k, v in updated_model.items():
            setattr(model, k, v)
        self.db.commit()
        self.db.refresh(model)
        return model
    
class StatisticRepository(BaseStatisticsRepository):
    def __init__(self, db: Session):
        super().__init__(db, StatisticModel)
