"""
Run this script once to create all database tables.
Safe to run multiple times — won't overwrite existing tables.
"""

from app.database.connection import engine, Base
from app.database.models import Prediction

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done. Tables created successfully.")