from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'test.db'}"


class UserCredentials(SQLModel, table=True):
    __tablename__ = "user_credentials"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: str = Field(index=True, unique=True)
    password: str


class Book(SQLModel, table=True):
    __tablename__ = "books"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    author: str = Field(index=True)
    published_year: int
    book_summary: str


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLModel.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


