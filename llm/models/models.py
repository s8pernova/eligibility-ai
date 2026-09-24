"""Health API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class DbPingResponse(BaseModel):
    status: str
    time: float
