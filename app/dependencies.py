from typing import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.
    Ensures the session is closed after completion of the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
