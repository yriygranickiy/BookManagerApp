from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app_bookmanager.models.bookmanager_models import Author,Book,Genre,Publisher,BookInstance,BookGenre,BookAuthor,PublisherBook

from alembic import context

from db.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
config.set_main_option('sqlalchemy.url', 'postgresql://my_user:qwerty@localhost:5433/book_db')

target_metadata = Base.metadata

def run_migrations_online() -> None:

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
