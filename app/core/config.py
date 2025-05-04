import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from app.core.firebase_config import FIREBASE_DATABASE_URL, FIREBASE_PROJECT_ID

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Base settings
    PROJECT_NAME: str = "NARRAPREP"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Performance
    WORKERS: int = int(os.getenv("WORKERS", 4))
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
    FIREBASE_DATABASE_URL: str = os.getenv("FIREBASE_DATABASE_URL", FIREBASE_DATABASE_URL)
    FIREBASE_PROJECT_ID: str = FIREBASE_PROJECT_ID
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 