from clients import get_openai_client
from fastapi import FastAPI

from backend.config import get_settings
from backend.models.health import HealthResponse
from backend.models.llm import LLMRequest, LLMResponse
from backend.services import health as health_service
from backend.services import llm as llm_service

settings = get_settings()
app = FastAPI(title=settings.TITLE, version=settings.VERSION)


client = get_openai_client()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return health_service.get_health()


@app.post("/llm", response_model=LLMResponse)
def llm(req: LLMRequest) -> LLMResponse:
    return llm_service.prompt(client, req, settings.LLM_MODEL)
