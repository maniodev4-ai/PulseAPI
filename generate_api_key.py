"""
Run this script to generate a new API key and store it in the database.

Usage:
    python generate_api_key.py "key name"

Example:
    python generate_api_key.py "usman-local-dev"
    python generate_api_key.py "team-member-ali"
"""

import sys
import secrets
from app.database.connection import engine, Base
from app.database.models import Prediction
from app.auth.models import APIKey
from sqlalchemy.orm import Session


def generate_key(name: str) -> str:
    """
    Generate a new API key, store it in the database, and print it.

    The raw key is printed ONCE and never stored — only the key
    itself is stored (for simplicity in v1; production would hash it).

    Args:
        name: A label identifying who this key is for.

    Returns:
        The generated API key string.
    """
    raw_key = secrets.token_urlsafe(32)

    with Session(engine) as db:
        record = APIKey(
            key_hash=raw_key,
            name=name,
            is_active=True,
        )
        db.add(record)
        db.commit()

    print(f"\n✓ API key generated for: '{name}'")
    print(f"\n  Key: {raw_key}\n")
    print("  Save this key — it will not be shown again.")
    print("  Pass it in requests as: X-API-Key: <key>\n")

    return raw_key


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_api_key.py 'key name'")
        sys.exit(1)

    name = sys.argv[1]
    generate_key(name)