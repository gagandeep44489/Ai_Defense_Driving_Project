"""Application configuration loaded from environment variables."""
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Runtime settings for API, workers, database, and security controls."""
    model_config = SettingsConfigDict(env_file='.env', env_prefix='SOVEREIGNAI_', extra='ignore')
    app_name: str = 'SovereignAI'
    environment: str = 'development'
    database_url: str = 'sqlite+pysqlite:///./sovereignai.db'
    redis_url: str = 'redis://redis:6379/0'
    jwt_secret_key: str = Field(default='change-me-in-production', min_length=16)
    jwt_algorithm: str = 'HS256'
    access_token_minutes: int = 30
    refresh_token_days: int = 7
    cors_origins: list[str] = ['http://localhost:8501', 'http://localhost:8000']
    rate_limit: str = '100/minute'

@lru_cache
def get_settings() -> Settings:
    """Return cached settings for dependency injection."""
    return Settings()
