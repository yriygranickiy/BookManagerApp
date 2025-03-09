import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, List, Generic, Type

from app_bookmanager.models.bookmanager_models import Author, Book, BookAuthor, Genre, BookGenre, Publisher, PublisherBook
from app_bookmanager.repositories.book_manager_repository import ABCBookAuthorManagerRepository, \
    BookManagerRepository, AuthorManagerRepository, GenreManagerRepository, PublisherManagerRepository, \
    BookInstanceRepository

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
    def update(self, model_id: uuid.UUID, model: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, model_id: uuid.UUID) -> None:
        raise NotImplementedError


class ManagerService(ABCBookAuthorManagerService):

    def __init__(self, repository: ABCBookAuthorManagerRepository):
        self.repository = repository

    def get_by_id(self, model_id: uuid.UUID) -> T:
        return self.repository.get_by_id(model_id)

    def get_all(self) -> list[T]:
        return self.repository.get_all()

    def create(self, model: T) -> None:
        self.repository.create(model)

    def update(self, model_id: uuid.UUID, model: dict) -> None:
        self.repository.update(model_id, model)

    def delete(self, model_id: uuid.UUID) -> None:
        self.repository.delete(model_id)


class BookManagerService(ManagerService):
    def __init__(self, repository: BookManagerRepository):
        super().__init__(repository)
        self.repository = repository

    def get_all_authors_from_book_by_title(self, book_title: str):
        return self.repository.get_related_entity(Book, Book.authors.key, Book.title.key, book_title)

    def add_author_to_book(self, author_id: uuid.UUID, book_id: uuid.UUID) -> None:
        self.repository.add_link_model_to_model(BookAuthor, book_id=book_id, author_id=author_id)

    def add_book_to_genre(self, book_id: uuid.UUID, genre_id: uuid.UUID) -> None:
        self.repository.add_link_model_to_model(BookGenre, book_id=book_id, genre_id=genre_id)

    def add_book_to_publisher(self, book_id: uuid.UUID, publisher_id: uuid.UUID) -> None:
        self.repository.add_link_model_to_model(PublisherBook, book_id=book_id, publisher_id=publisher_id)


class AuthorManagerService(ManagerService):
    def __init__(self, repository: AuthorManagerRepository):
        super().__init__(repository)
        self.repository = repository

    def get_all_books_written_author_by_last_name(self, author_last_name: str):
        return self.repository.get_related_entity(Author, Author.books.key, Author.last_name.key, author_last_name)

    def add_book_to_author(self, author_id: uuid.UUID, book_id: uuid.UUID) -> None:
        self.repository.add_link_model_to_model(BookAuthor, book_id=book_id, author_id=author_id)


class GenreManagerService(ManagerService):
    def __init__(self, repository: GenreManagerRepository):
        super().__init__(repository)
        self.repository = repository

    def get_books_by_genre(self, genre: str):
        return self.repository.get_related_entity(Genre, Genre.books.key, Genre.title.key, genre)


class PublisherManagerService(ManagerService):
    def __init__(self, repository: PublisherManagerRepository):
        super().__init__(repository)
        self.repository = repository

    def get_books_by_publisher(self, publisher: str):
        return self.repository.get_related_entity(Publisher, Publisher.books.key, Publisher.title.key, publisher)


class BookInstanceService(BookManagerService):
    def __init__(self, repository: BookInstanceRepository):
        super().__init__(repository)
        self.repository = repository
