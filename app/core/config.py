import os
from typing import List, Optional
from dotenv import load_dotenv


load_dotenv()

class Settings:
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY") 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    COMPILER_API_URL = os.getenv("COMPILER_API_URL")
    CLIENT_ORIGINS: List[str] = [
        origin.strip() for origin in os.getenv("CLIENT_ORIGINS", "").split(",") if origin.strip()
    ]
    

class DevelopmentSettings(Settings):
    USER = os.getenv("LOCAL_USER")
    PASSWORD = os.getenv("LOCAL_PASSWORD")
    HOST = os.getenv("LOCAL_HOST")
    PORT = os.getenv("LOCAL_PORT")
    DBNAME = os.getenv("LOCAL_DBNAME")


class ProductionSettings(Settings):
    USER = os.getenv("PRODUCTION_USER")
    PASSWORD = os.getenv("PRODUCTION_PASSWORD")
    HOST = os.getenv("PRODUCTION_HOST")
    PORT = os.getenv("PRODUCTION_PORT")
    DBNAME = os.getenv("PRODUCTION_DBNAME")


def get_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "development").lower()
    if env == "production":
        return ProductionSettings()
    return DevelopmentSettings()

settings = get_settings()


