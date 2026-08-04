"""
Database connection setup for PulseAPI.

Creates the SQLAlchemy engine and session factory that the rest
of the application uses to talk to PostgreSQL.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Make sure your .env file exists and contains DATABASE_URL."
    )

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """
    Base class for all database models.
    Every table definition will inherit from this.
    """
    pass