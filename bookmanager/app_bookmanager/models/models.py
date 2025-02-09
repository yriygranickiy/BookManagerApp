import uuid


from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from bookmanager.db.database import Base


class BookAuthor(Base):
    __tablename__ = 'book_author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('authors.id'), nullable=False)

class Book(Base):
    __tablename__ = 'books'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(50), nullable=False)
    numbers_page = Column(Integer, nullable=False)
    authors = relationship('Author', secondary='book_author', back_populates='books')
    genres = relationship('Genre', secondary='book_genre', back_populates='books')
    publishers = relationship('Publisher', secondary='publisher_book', back_populates='books')

class Author(Base):
    __tablename__ = 'authors'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    books = relationship('Book', secondary='book_author', back_populates='authors')

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(50), nullable=False)
    books = relationship('Book', secondary='', back_populates='genres')

class BookGenre(Base):
    __tablename__ = 'genre_book'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'), nullable=False)
    genre_id = Column(UUID(as_uuid=True), ForeignKey('genres.id'), nullable=False)

class BookInstance(Base):
    __tablename__ = 'book_instances'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'), nullable=False)
    status = Column(String, nullable=False)

class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    books = relationship('Book', secondary='publisher_book', back_populates='publishers')

class PublisherBook(Base):
    __tablename__ = 'publisher_book'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    publisher_id = Column(UUID(as_uuid=True), ForeignKey('publishers.id'), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'), nullable=False)

