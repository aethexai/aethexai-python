"""SDK exception hierarchy."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any


class AethexError(Exception):
    """Base exception for all SDK errors."""


class APIConnectionError(AethexError):
    """Raised when a network error prevents the request from completing."""

    def __init__(self, message: str = "Connection error", *, cause: Exception | None = None):
        self.cause = cause
        super().__init__(message)


class APITimeoutError(APIConnectionError):
    """Raised when the request times out."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message)


class APIStatusError(AethexError):
    """Raised when the API returns an error HTTP status."""

    def __init__(
        self,
        message: str = "",
        *,
        code: str = "internal_error",
        status_code: int = 500,
        response: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.response = response or {}
        self.headers = headers or {}
        super().__init__(message)

    @classmethod
    def from_response(
        cls,
        status_code: int,
        body: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> APIStatusError:
        error_msg = body.get("detail", body.get("error", "Unknown error"))
        if isinstance(error_msg, list):
            error_msg = "; ".join(str(e) for e in error_msg)
        error_code = body.get("code", "internal_error")

        exc_class = _STATUS_MAP.get(status_code, APIStatusError)
        return exc_class(
            message=str(error_msg),
            code=error_code,
            status_code=status_code,
            response=body,
            headers=headers,
        )


class AuthenticationError(APIStatusError):
    """401 - invalid or missing API key."""


class PermissionDeniedError(APIStatusError):
    """403 - insufficient permissions or scopes."""


class NotFoundError(APIStatusError):
    """404 - resource not found."""


class ConflictError(APIStatusError):
    """409 - resource already exists."""


class ValidationError(APIStatusError):
    """422 - request validation failed."""


class RateLimitError(APIStatusError):
    """429 - rate limit exceeded."""

    @property
    def retry_after(self) -> float | None:
        header_val = self.headers.get("retry-after") or self.headers.get("Retry-After")
        if header_val:
            try:
                return float(header_val)
            except (ValueError, TypeError):
                pass
        return self.response.get("retry_after")


class InternalServerError(APIStatusError):
    """5xx - server-side error."""


_STATUS_MAP: dict[int, type[APIStatusError]] = {
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
    429: RateLimitError,
    500: InternalServerError,
    502: InternalServerError,
    503: InternalServerError,
    504: InternalServerError,
}


def _map_status_to_exception(
    status_code: int,
    body: bytes | str | dict[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
) -> APIStatusError:
    """Build an APIStatusError subclass instance for a non-2xx HTTP response.

    ``body`` may be raw bytes (typical from ``httpx.Response.content``), a
    pre-decoded string, an already-parsed JSON dict, or ``None``. The function
    is tolerant: if the body cannot be parsed as JSON it still produces a
    well-formed exception that surfaces the raw text for debugging.
    """
    parsed: dict[str, Any]
    if body is None:
        parsed = {}
    elif isinstance(body, dict):
        parsed = body
    else:
        raw = body.decode("utf-8", errors="replace") if isinstance(body, bytes) else body
        try:
            decoded = json.loads(raw) if raw else {}
        except (ValueError, TypeError):
            decoded = {"detail": raw[:500] if raw else "Unknown error"}
        parsed = decoded if isinstance(decoded, dict) else {"detail": decoded}

    headers_dict: dict[str, str] | None
    if headers is None:
        headers_dict = None
    elif isinstance(headers, dict):
        headers_dict = headers
    else:
        headers_dict = {k: v for k, v in headers.items()}

    return APIStatusError.from_response(status_code, parsed, headers_dict)
