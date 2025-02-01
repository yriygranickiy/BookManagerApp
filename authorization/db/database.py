from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://my_user:qwerty@localhost:5433/auth_db"

engine = create_engine(DATABASE_URL, echo=True, isolation_level="AUTOCOMMIT")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()