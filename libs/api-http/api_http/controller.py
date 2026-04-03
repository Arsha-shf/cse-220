"""Controller base class and response helper methods."""

from __future__ import annotations

from typing import Any

from django.http import HttpRequest

from .responses import (
    CreatedResponse,
    ErrorResponse,
    JsonApiResponse,
    NoContentResponse,
    OkResponse,
)


class Controller:
    """Base class for class-based endpoint handlers."""

    def __init__(self, request: HttpRequest | None):
        self.request = request

    def json(
        self,
        payload: Any,
        *,
        status: int = 200,
        headers: dict[str, str] | None = None,
    ) -> JsonApiResponse:
        """Return JSON payload with explicit status and headers."""

        return JsonApiResponse(payload, status=status, headers=headers)

    def ok(self, payload: Any, *, headers: dict[str, str] | None = None) -> OkResponse:
        """Return a successful JSON response (HTTP 200)."""

        return OkResponse(payload, headers=headers)

    def created(
        self,
        payload: Any,
        *,
        headers: dict[str, str] | None = None,
    ) -> CreatedResponse:
        """Return a resource-created JSON response (HTTP 201)."""

        return CreatedResponse(payload, headers=headers)

    def no_content(self, *, headers: dict[str, str] | None = None) -> NoContentResponse:
        """Return a no-content response (HTTP 204)."""

        return NoContentResponse(headers=headers)

    def error(
        self,
        *,
        status: int,
        code: str,
        message: str,
        details: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> ErrorResponse:
        """Return a standardized JSON error response."""

        return ErrorResponse(
            status=status,
            error_code=code,
            message=message,
            details=details,
            headers=headers,
        )
