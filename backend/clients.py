"""Client dependencies."""

from functools import lru_cache

from openai import OpenAI

from .config import get_settings

settings = get_settings()


@lru_cache
def get_openai_client() -> OpenAI:
    """Get cached OpenAI client instance."""
    settings = get_settings()
    return OpenAI(api_key=settings.openai_api_key_str)
