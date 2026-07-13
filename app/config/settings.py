from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="CLIMATESHIELD_")
    app_name: str = "ClimateShield AI Recommendation Engine"
    environment: str = "development"
    jwt_secret_key: str = "change-me"
    cors_origins: list[str] = ["*"]
    redis_url: str = "redis://redis:6379/0"
    database_url: str = "postgresql+psycopg://postgres:postgres@postgres:5432/climateshield"


settings = Settings()
