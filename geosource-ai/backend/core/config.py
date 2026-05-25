"""Application configuration."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GeoSource AI"
    api_prefix: str = "/api/v1"
    log_level: str = "INFO"
    data_path: str = "data/processed/suppliers.csv"
    model_path: str = "models/risk_model.joblib"
    preprocessor_path: str = "models/preprocessor.joblib"
    label_encoder_path: str = "models/label_encoder.joblib"
    graph_path: str = "models/supplier_graph.joblib"
    model_version: str = "1.1.0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
