import uuid


from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from db.database import Base


class BookAuthor(Base):
    __tablename__ = 'book_author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('authors.id'), nullable=False)
    #
    # books = relationship("Book", back_populates="book_authors")
    # authors = relationship("Author", back_populates="author_books")
class Book(Base):
    __tablename__ = 'books'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(50), nullable=False)
    authors = relationship('Author', secondary='book_author', back_populates='books')

class Author(Base):
    __tablename__ = 'authors'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    books = relationship('Book', secondary='book_author', back_populates='authors')

