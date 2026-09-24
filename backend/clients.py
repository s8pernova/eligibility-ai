"""Client dependencies."""

from functools import lru_cache

from openai import OpenAI

from backend.config import get_settings


@lru_cache
def get_openai_client() -> OpenAI:
    """Get a cached client with bounded timeout and retries."""
    settings = get_settings()
    return OpenAI(api_key=settings.openai_api_key_str, timeout=30.0, max_retries=1)
