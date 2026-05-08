from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Meeting Brain"
    environment: str = Field(default="development", alias="ENVIRONMENT")
    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@db:5432/meeting_brain", alias="DATABASE_URL")
    jwt_secret_key: str = Field(default="change-me-in-production", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    azure_openai_endpoint: str | None = Field(default=None, alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str | None = Field(default=None, alias="AZURE_OPENAI_API_KEY")
    azure_openai_deployment: str = Field(default="gpt-4o-mini", alias="AZURE_OPENAI_DEPLOYMENT")
    embedding_model: str = Field(default="text-embedding-3-small", alias="OPENAI_EMBEDDING_MODEL")
    vector_store_path: str = Field(default="/data/chroma", alias="VECTOR_STORE_PATH")
    upload_dir: str = Field(default="/data/uploads", alias="UPLOAD_DIR")
    smtp_host: str | None = Field(default=None, alias="SMTP_HOST")
    smtp_from: str = Field(default="noreply@meetingbrain.local", alias="SMTP_FROM")


@lru_cache
def get_settings() -> Settings:
    return Settings()
