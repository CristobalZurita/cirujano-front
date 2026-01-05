"""
Configuration settings for Cirujano de Sintetizadores API
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    api_title: str = "Cirujano de Sintetizadores API"
    api_version: str = "1.0.0"
    debug: bool = False

    # Database Configuration
    database_url: str = "sqlite:///./cirujano.db"
    database_echo: bool = False

    # JWT Configuration
    secret_key: str = "your-secret-key-change-in-production"
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
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
