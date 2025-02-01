import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Type, Union

from sqlalchemy.orm import Session, joinedload, DeclarativeMeta

from bookmanager.app.models.models import Book, Author, BookAuthor

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
    def update(self, model: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, model: T) -> None:
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

    def update(self, model: T) -> None:
        pass

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

    # def add_author_to_book(self, author_id: uuid.UUID, book_id: uuid.UUID) -> None:
    #     book_author = BookAuthor(book_id=book_id, author_id=author_id)
    #     self.db.add(book_author)
    #     self.db.commit()


class AuthorManagerRepository(BaseBookAuthorRepository):
    def __init__(self, db: Session):
        super().__init__(db, Author)

    # def add_book_to_author(self, author_id: uuid.UUID, book_id: uuid.UUID) -> None:
    #     author_book = BookAuthor(book_id=book_id, author_id=author_id)
    #     self.db.add(author_book)
    #     self.db.commit()
