# backend/app/core/config.py
import json
import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    FIREBASE_CREDENTIALS: str
    DEBUG: bool = True
    
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
        extra = "ignore"  # This allows extra fields in .env without validation errors

settings = Settings()