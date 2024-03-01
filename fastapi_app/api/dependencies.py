from pathlib import Path
from typing import Generator

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy import create_engine


FILE_PATH = Path(__file__).relative_to(Path.cwd())

DATABASE_URL = "sqlite:///./books_riitude.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()



def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed with error {e.__str__()}",
        )
    finally:
        db.close()
