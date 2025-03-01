import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Type, Union

from sqlalchemy.orm import Session, joinedload, DeclarativeMeta

from app_bookmanager.models.models import Book, Author, Genre, Publisher, BookInstance

T = TypeVar('T')


class ABCBookAuthorManagerRepository(ABC, Generic[T]):

    @abstractmethod
    def get_by_id(self, model_id: uuid.UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def create(self, model: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, model_id: uuid.UUID, updated_model: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, model_id: uuid.UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_link_model_to_model(self, model: Type[DeclarativeMeta], **fields) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_related_entity(self, entity: Type[Union[T, T]],
                           related_field: str,
                           filter_field: str,
                           filter_value: Union[uuid.UUID, str]):
        raise NotImplementedError


class BaseBookAuthorRepository(ABCBookAuthorManagerRepository):

    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, model_id: uuid.UUID) -> T:
        return self.db.query(self.model).filter_by(id=model_id).first()

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def create(self, model: T) -> None:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

    def update(self, model_id: uuid.UUID, updated_model: dict):
        model = self.db.query(self.model).filter_by(id=model_id).first()
        if not model:
            return None
        for k, v in updated_model.items():
            setattr(model, k, v)
        self.db.commit()
        self.db.refresh(model)
        return model

    def delete(self, model_id: uuid.UUID) -> None:
        model = self.db.query(self.model).filter_by(id=model_id).first()
        self.db.delete(model)
        self.db.commit()

    def get_related_entity(self, entity: T,
                           related_field: Union[T],
                           filter_field: Union[T],
                           filter_value: Union[uuid.UUID, str]):
        return (
            self.db.query(entity)
            .options(joinedload(getattr(entity, related_field)))
            .filter(getattr(entity, filter_field) == filter_value)
            .first()
        )

    def add_link_model_to_model(self, model: Type[DeclarativeMeta], **fields) -> None:
        exists = self.db.query(model).filter_by(**fields).first()
        if not exists:
            data = model(**fields)
            self.db.add(data)
            self.db.commit()
        else:
            print(f'The relationship is already exists!')


class BookManagerRepository(BaseBookAuthorRepository):
    def __init__(self, db: Session):
        super().__init__(db, Book)


class AuthorManagerRepository(BaseBookAuthorRepository):
    def __init__(self, db: Session):
        super().__init__(db, Author)


class GenreManagerRepository(BaseBookAuthorRepository):
    def __init__(self, db: Session):
        super().__init__(db, Genre)


class PublisherManagerRepository(BaseBookAuthorRepository):
    def __init__(self, db: Session):
        super().__init__(db, Publisher)


class BookInstanceRepository(BaseBookAuthorRepository):
    def __init__(self, db: Session):
        super().__init__(db, BookInstance)
