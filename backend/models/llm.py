"""LLM API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class LLMRequest(BaseModel):
    response: str


class LLMResponse(BaseModel):
    response: str
