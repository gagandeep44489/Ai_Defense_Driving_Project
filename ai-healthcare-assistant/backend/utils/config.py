from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Healthcare Assistant"
    environment: str = "development"
    log_level: str = "INFO"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    postgres_url: str = "postgresql+psycopg2://postgres:postgres@postgres:5432/healthcare"
    vector_top_k: int = 3

    whisper_model_name: str = "whisper-1"
    supported_languages: str = "en,hi"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
