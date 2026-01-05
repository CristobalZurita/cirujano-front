"""
Configuration settings for Cirujano de Sintetizadores API
"""

from pydantic import BaseModel
from functools import lru_cache
from typing import Optional
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings(BaseModel):
    """Application settings"""

    # API Configuration
    api_title: str = "Cirujano de Sintetizadores API"
    api_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./cirujano.db")
    database_echo: bool = False

    # JWT Configuration
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS Configuration
    allowed_origins: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Email Configuration
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: Optional[str] = None

    # Pricing Configuration
    diagnostic_fee: int = 0  # Free diagnostic
    service_multipliers: dict = {
        "legendary": 1.8,
        "professional": 1.5,
        "standard": 1.2,
        "specialized": 1.3,
        "boutique": 1.4,
        "historic": 1.3,
    }

    value_multipliers: dict = {
        "low": 1.0,  # < 500000 CLP
        "medium": 1.3,  # 500000 - 2000000 CLP
        "high": 1.6,  # 2000000 - 5000000 CLP
        "premium": 2.0,  # > 5000000 CLP
    }
    class Config:
        case_sensitive = False


# Instantiate settings with environment variables
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance"""
    return settings
