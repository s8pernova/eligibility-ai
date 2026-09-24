from fastapi import FastAPI

from config import get_settings
from llm.models.health import HealthResponse

settings = get_settings()
app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return {"status": "ok"}
