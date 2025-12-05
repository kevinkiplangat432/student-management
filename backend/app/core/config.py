from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    FIREBASE_CREDENTIALS: str
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    DEBUG: bool = False
    
    @property
    def cors_origins(self):
        if self.DEBUG:
            return ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"]
        else:
            return self.BACKEND_CORS_ORIGINS

    class Config:
        env_file = ".env"

settings = Settings()