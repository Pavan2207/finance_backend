import json
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Use sample DB for Vercel/demo (no real DB needed)
SAMPLE_DB_PATH = "sample_db.json"
if os.path.exists(SAMPLE_DB_PATH):
    DATABASE_URL = "sqlite:///:memory:"  # In-memory for demo
else:
    DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load sample data on startup if sample_db.json exists
if Path(SAMPLE_DB_PATH).exists():
    # Note: Load logic in main.py or service
    pass
