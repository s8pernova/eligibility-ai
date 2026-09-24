import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    TITLE = "Eligibility AI"
    VERSION = "0.1.0"


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
