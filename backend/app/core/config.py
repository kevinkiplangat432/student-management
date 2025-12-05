# import setting management
# 
from pydantic_settings import BaseSettings # handleenvironment varialbles with validation
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    FIREBASE_CREDENTIALS: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
