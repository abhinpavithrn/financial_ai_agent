"""Configuration settings for the Financial AI Agent."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    FINNHUB_API_KEY: str
    OPENAI_API_KEY: str
    
    # Database
    DATABASE_URL: str = "sqlite:///./financial_ai.db"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # LLM Settings
    MODEL_NAME: str = "gpt-4-turbo-preview"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1500
    
    # Cache TTL (seconds)
    STOCK_PRICE_CACHE_TTL: int = 60  # 1 minute
    NEWS_CACHE_TTL: int = 300  # 5 minutes
    COMPANY_PROFILE_CACHE_TTL: int = 86400  # 24 hours
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
