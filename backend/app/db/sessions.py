# sessions.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.core.config import settings

# Check DATABASE_URL
if not settings.DATABASE_URL:
    error_msg = "DATABASE_URL is not configured. Please check your environment variables."
    print(f"❌ {error_msg}")
    print(f"Available environment variables:")
    for key in ["DATABASE_URL", "PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD"]:
        value = os.getenv(key)
        if value:
            print(f"  {key}: {'*' * 8 if 'PASSWORD' in key else value[:50]}")
    raise ValueError(error_msg)

print(f" Using DATABASE_URL: {settings.DATABASE_URL[:50]}...")

engine = create_engine(
    settings.DATABASE_URL, 
    echo=False,  # Set to False in production
    pool_pre_ping=True,  # Optional: helps with connection issues
    pool_recycle=300  # Optional: recycle connections after 5 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()