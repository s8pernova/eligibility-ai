"""HTTP endpoints for the eligibility backend."""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from openai import (
    APIError,
    APITimeoutError,
    ContentFilterFinishReasonError,
    LengthFinishReasonError,
    OpenAI,
    RateLimitError,
)
from pydantic import ValidationError

from backend.clients import get_openai_client
from backend.config import get_settings
from backend.models.health import HealthResponse
from backend.models.llm import LLMRequest, LLMResponse
from backend.services import health as health_service
from backend.services import llm as llm_service

settings = get_settings()
app = FastAPI(title=settings.TITLE, version=settings.VERSION)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return health_service.get_health()


@app.post("/llm", response_model=LLMResponse)
def llm(
    req: LLMRequest, client: Annotated[OpenAI, Depends(get_openai_client)]
) -> LLMResponse:
    try:
        return llm_service.prompt(client, req, settings.LLM_MODEL)
    except APITimeoutError as exc:
        raise HTTPException(504, "Eligibility provider timed out.") from exc
    except RateLimitError as exc:
        raise HTTPException(
            503, "Eligibility provider is temporarily unavailable."
        ) from exc
    except (
        APIError,
        LengthFinishReasonError,
        ContentFilterFinishReasonError,
        ValidationError,
        llm_service.LLMOutputError,
    ) as exc:
        raise HTTPException(
            502, "Eligibility provider returned no usable assessment."
        ) from exc
