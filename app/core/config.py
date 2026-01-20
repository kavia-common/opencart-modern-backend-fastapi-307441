"""
Configuration Management
Centralized settings using environment variables
"""
from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Application configuration settings.
    Loads from environment variables or .env file.
    """
    # Application
    APP_NAME: str = "OpenCart Modern API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Logging
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FORMAT: str = "text"  # text or json
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/opencart.db"
    
    # Security - USER MUST PROVIDE SECRET_KEY
    # This should be a random string of at least 32 characters
    SECRET_KEY: str = "CHANGE-THIS-TO-A-RANDOM-SECRET-KEY-MIN-32-CHARS"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # CORS - can be provided as comma-separated string or JSON array
    ALLOWED_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse ALLOWED_ORIGINS from comma-separated string or list."""
        if isinstance(v, str):
            # Split by comma and strip whitespace
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = 'ignore'  # Allow extra environment variables without validation errors


settings = Settings()
