"""
Database connection setup.
Reads DATABASE_URL from .env and creates the SQLAlchemy engine + session.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./matdatahub_dev.db")

# Supabase gives "postgres://..." but SQLAlchemy needs "postgresql://..."
if DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://"):
    # SQLAlchemy 2.0+ highly recommends psycopg3. 
    # Force the dialect to use postgresql+psycopg if not already set.
    if not DATABASE_URL.startswith("postgresql+"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# For SQLite, we need connect_args to allow multi-threaded access
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All models inherit from this
Base = declarative_base()


def get_db():
    """
    Dependency for FastAPI routes.
    Opens a DB session, yields it, then closes it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
