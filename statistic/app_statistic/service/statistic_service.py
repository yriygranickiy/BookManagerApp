import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

import consumer_service

from app_statistic.repository.statistic_repository import ABCStatisticsManagerRepository, StatisticsRepository

T = TypeVar('T')

class ABCStatisticManagerService(ABC, Generic[T]):

    @abstractmethod
    def get_by_id(self, model_id: uuid.UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def create(self, model: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, model_id: uuid.UUID, model: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, model_id: uuid.UUID) -> None:
        raise NotImplementedError


class BaseStatisticService(ABCStatisticManagerService):

    def __init__(self, repository: ABCStatisticsManagerRepository):
        self.repository = repository

    def get_by_id(self, model_id: uuid.UUID) -> T:
        return self.repository.get_by_id(model_id)

    def get_all(self) -> list[T]:
        return self.repository.get_all()

    def create(self, model: T) -> None:
        return self.repository.create(model)

    def update(self, model_id: uuid.UUID, model: dict) -> None:
        self.repository.update(model_id, model)

    def delete(self, model_id: uuid.UUID) -> None:
        self.repository.delete(model_id)

class StatisticService(BaseStatisticService):
    def __init__(self, repository: StatisticsRepository):
        super().__init__(repository)
        self.repository = repository




