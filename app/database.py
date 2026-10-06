"""
Database connection setup.
Reads DATABASE_URL from .env and creates the SQLAlchemy engine + session.
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./matdatahub_dev.db")

print(f"[database.py] Raw DATABASE_URL scheme: {DATABASE_URL.split('@')[0].split('://')[0] if '://' in DATABASE_URL else 'unknown'}", flush=True)

# Supabase gives "postgres://..." but SQLAlchemy needs "postgresql://..."
# Force psycopg2 dialect to guarantee compatibility with psycopg2-binary
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql+"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql+psycopg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql+psycopg2://", 1)

# For SQLite, we need connect_args to allow multi-threaded access
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    print("[database.py] Using SQLite engine", flush=True)
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,        # Recycle connections every 30 min (Supabase can drop idle ones)
        connect_args={
            "connect_timeout": 5,  # Fail fast: 5 seconds max to connect
            "options": "-c statement_timeout=10000"  # 10 second query timeout
        }
    )
    print("[database.py] Using PostgreSQL engine (pooler)", flush=True)

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
