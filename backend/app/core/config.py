# config.py
import os
import json
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Build DATABASE_URL from Render's environment variables if available
    @property
    def DATABASE_URL(self) -> str:
        # First, try direct DATABASE_URL
        db_url = os.getenv("DATABASE_URL", "")
        if db_url:
            return db_url
        
        # Build from Render's PostgreSQL environment variables
        if all([
            os.getenv("PGHOST"),
            os.getenv("PGDATABASE"),
            os.getenv("PGUSER"),
            os.getenv("PGPASSWORD")
        ]):
            return f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@{os.getenv('PGHOST')}:{os.getenv('PGPORT', '5432')}/{os.getenv('PGDATABASE')}"
        
        return ""
    
    FIREBASE_CREDENTIALS: str = ""
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins from environment variable or default."""
        cors_str = os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:5173", "http://localhost:3000"]')
        try:
            # Try to parse as JSON
            return json.loads(cors_str.replace("'", '"'))
        except json.JSONDecodeError:
            # If not JSON, return default
            return ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()