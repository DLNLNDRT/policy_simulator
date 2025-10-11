"""
Configuration management for Policy Simulation Assistant
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Policy Simulation Assistant"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # Server
    BACKEND_HOST: str = Field(default="0.0.0.0", env="BACKEND_HOST")
    BACKEND_PORT: int = Field(default=8000, env="BACKEND_PORT")
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./data/health_indicators.db",
        env="DATABASE_URL"
    )
    
    # AI Integration
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = Field(
        default="claude-3-sonnet-20240229",
        env="ANTHROPIC_MODEL"
    )
    
    # Data Sources
    WHO_DATA_API_KEY: Optional[str] = Field(default=None, env="WHO_DATA_API_KEY")
    WORLD_BANK_API_KEY: Optional[str] = Field(default=None, env="WORLD_BANK_API_KEY")
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    JWT_SECRET: str = Field(
        default="your-jwt-secret-change-in-production",
        env="JWT_SECRET"
    )
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        env="CORS_ORIGINS"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        env="ALLOWED_HOSTS"
    )
    
    # Monitoring & Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    
    # Performance
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    MAX_SIMULATIONS_PER_HOUR: int = Field(default=1000, env="MAX_SIMULATIONS_PER_HOUR")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # Data Quality
    MIN_DATA_QUALITY_SCORE: float = Field(default=90.0, env="MIN_DATA_QUALITY_SCORE")
    MAX_SIMULATION_RESPONSE_TIME: int = Field(default=5, env="MAX_SIMULATION_RESPONSE_TIME")  # seconds
    
    # Cost Management
    MAX_COST_PER_SIMULATION: float = Field(default=0.10, env="MAX_COST_PER_SIMULATION")  # USD
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
