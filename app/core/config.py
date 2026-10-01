import os
from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_database_url() -> str:
    return "postgresql+psycopg://postgres:postgres@localhost:5433/app"


class Settings(BaseSettings):
    app_name: str = "ai-image-matching-engine"
    app_env: str = "development"
    app_debug: bool = True
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5433/app"
    database_echo: bool = False
    gemini_api_key: str = ""
    gemini_vision_model: str = "gemini-1.5-flash"
    gemini_embedding_model: str = "text-embedding-004"
    vision_confidence_threshold: float = 0.72
    match_similarity_threshold: float = 0.35
    ai_retry_count: int = 3
    ai_retry_delay_seconds: int = 2
    corpus_dir: str = "./data/corpus"
    seed_data_path: str = "./data/seed"
    postgres_db: str = "app"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str | None) -> str | None:
        if value is None:
            return _default_database_url()
        if isinstance(value, str):
            if "@localhost:5432" in value:
                return value.replace("@localhost:5432", "@localhost:5433")
            if value == "postgresql+psycopg://postgres:postgres@localhost/app":
                return "postgresql+psycopg://postgres:postgres@localhost:5433/app"
        return value


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if os.getenv("DATABASE_URL", "").startswith("postgresql+psycopg://postgres:postgres@localhost:5432"):
        os.environ["DATABASE_URL"] = settings.database_url
    return settings
