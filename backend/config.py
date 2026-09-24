import os
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
    )

    # Metadata
    TITLE: Annotated[str, Field(description="The name of the application.")] = (
        "Eligibility AI"
    )
    VERSION: Annotated[
        str, Field(description="The current version of the application.")
    ] = "0.1.0"

    # API
    OPENAI_API_KEY: Annotated[
        SecretStr,
        Field(
            description="API key for OpenAI services (e.g., LLM extraction, embeddings)."
        ),
    ]

    # LLM
    LLM_MODEL: Annotated[
        str, Field(description="The model used to assess scholarship eligibility.")
    ] = "gpt-4o-mini"

    @property
    def openai_api_key_str(self) -> str:
        return self.OPENAI_API_KEY.get_secret_value()


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    env_file = os.getenv("ENV_FILE")

    if not env_file:
        environment = os.getenv("ENVIRONMENT", "local").lower()
        local_env = BASE_DIR / ".env"
        if environment in {"local", "dev", "development"} and local_env.exists():
            env_file = str(local_env)

    return Settings(_env_file=env_file or None)
