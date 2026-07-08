import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Retrieve Database URL from environment, fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitness_booking.db")

# Configure connection arguments, specifically for SQLite multithreading support
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Declarative Base for models
Base = declarative_base()
