"""
Authentication dependency for PulseAPI.

Provides the get_api_key() dependency function that validates
incoming API keys on every protected request.
"""

from fastapi import Security, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.auth.models import APIKey

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_db():
    """Provide a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_api_key(
    api_key: str = Security(API_KEY_HEADER),
    db: Session = Depends(get_db),
) -> APIKey:
    """
    Validate the API key from the X-API-Key header.

    Looks up the raw key against all active keys in the database.
    Returns the matching APIKey record if valid.

    Raises:
        HTTPException: 401 if no key provided or key is invalid/inactive.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Pass it in the X-API-Key header.",
        )

    active_keys = db.query(APIKey).filter(APIKey.is_active == True).all()
    for key_record in active_keys:
        if key_record.key_hash == api_key:
            return key_record

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or inactive API key.",
    )