"""Health API service functions."""

from __future__ import annotations

from backend.models.health import HealthResponse


def get_health() -> HealthResponse:
    """Return process health."""
    return HealthResponse(status="ok")
