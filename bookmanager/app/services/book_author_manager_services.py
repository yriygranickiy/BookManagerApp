import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, List, Generic, Type

from bookmanager.app.models.models import Author, Book, BookAuthor
from bookmanager.app.repositories.book_author_manager_repository import ABCBookAuthorManagerRepository, \
    BookManagerRepository, AuthorManagerRepository
from bookmanager.app.schemas.book_author_manager_schemas import AuthorBooksResponse

T = TypeVar('T')


class ABCBookAuthorManagerService(ABC, Generic[T]):

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
    def update(self, model_id: uuid.UUID, model: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, model_id: uuid.UUID) -> None:
        raise NotImplementedError


class BookAuthorManagerService(ABCBookAuthorManagerService):

    def __init__(self, repository: ABCBookAuthorManagerRepository):
        self.repository = repository

    def get_by_id(self, model_id: uuid.UUID) -> T:
        return self.repository.get_by_id(model_id)

    def get_all(self) -> List[T]:
        return self.repository.get_all()

    def create(self, model: T) -> None:
        self.repository.create(model)

    def update(self, model_id: uuid.UUID, model: T) -> None:
        pass

    def delete(self, model_id: uuid.UUID) -> None:
        self.repository.delete(model_id)


class BookManagerService(BookAuthorManagerService):
    def __init__(self, repository: BookManagerRepository):
        super().__init__(repository)
        self.repository = repository

    def get_all_authors_from_book_by_title(self, book_title: str) -> List[T]:
        return self.repository.get_related_entity(Book, Book.authors.key, Book.title.key, book_title)

    def add_author_to_book(self, author_id: uuid.UUID, book_id: uuid.UUID) -> None:
        self.repository.add_link_model_to_model(BookAuthor, book_id=book_id, author_id=author_id)


class AuthorManagerService(BookAuthorManagerService):
    def __init__(self, repository: AuthorManagerRepository):
        super().__init__(repository)
        self.repository = repository

    def get_all_books_written_author_by_id(self, author_id: uuid.UUID) -> T:
        return self.repository.get_related_entity(Author, Author.books.key, Author.id.key, author_id)

    def add_book_to_author(self, author_id: uuid.UUID, book_id: uuid.UUID) -> None:
        self.repository.add_link_model_to_model(BookAuthor, book_id=book_id, author_id=author_id)
