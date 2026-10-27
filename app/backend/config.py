"""
FraudLens: Application Configuration & Environment Settings
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "FraudLens AI-Powered Fraud Detection & Investigation"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api"
    
    # Oracle Configuration
    ORACLE_USER: str = os.getenv("ORACLE_USER", "FRAUDLENS_USER")
    ORACLE_PASSWORD: str = os.getenv("ORACLE_PASSWORD", "FraudLens2026#")
    ORACLE_DSN: str = os.getenv("ORACLE_DSN", "localhost:1521/freepdb1")
    ORACLE_HOST: str = os.getenv("ORACLE_HOST", "localhost")
    ORACLE_PORT: int = int(os.getenv("ORACLE_PORT", "1521"))
    ORACLE_SERVICE: str = os.getenv("ORACLE_SERVICE", "freepdb1")
    ORACLE_POOL_MIN: int = 1
    ORACLE_POOL_MAX: int = 5
    
    # Fraud Surveillance Rule Engine Settings
    HIGH_AMOUNT_THRESHOLD: float = float(os.getenv("HIGH_AMOUNT_THRESHOLD", "50000.0"))
    
    # Server & Security
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Graceful Fallback Mode if Oracle is not started
    DEMO_MODE_FALLBACK: bool = True

    # Convenient property aliases
    @property
    def app_name(self) -> str:
        return self.PROJECT_NAME

    @property
    def app_version(self) -> str:
        return self.VERSION

    @property
    def oracle_password(self) -> str:
        return self.ORACLE_PASSWORD

    @property
    def cors_origins_list(self) -> List[str]:
        return self.CORS_ORIGINS

    @property
    def high_amount_threshold(self) -> float:
        return self.HIGH_AMOUNT_THRESHOLD
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
