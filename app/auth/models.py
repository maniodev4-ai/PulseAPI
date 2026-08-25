"""
Database model for API keys.

Defines the api_keys table that stores hashed API keys
and their metadata.
"""

from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class APIKey(Base):
    """
    Represents one API key in the database.

    Keys are stored hashed — the raw key is only shown once
    at generation time and never stored in plain text.
    """

    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key_hash: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, server_default=text("NOW()"), nullable=False
    )