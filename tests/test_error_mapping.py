"""Unit tests for `_map_status_to_exception` and the wrapper `_call` helpers.

These tests cover the silent-failure bug fix: every wrapper method on
``AethexAI``, ``AsyncAethexAI``, and ``Kora`` must now raise a typed
exception on non-2xx responses instead of returning ``None``.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from aethexai import (
    AethexAI,
    APIStatusError,
    AsyncAethexAI,
    AuthenticationError,
    ConflictError,
    InternalServerError,
    Kora,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ValidationError,
)
from aethexai._exceptions import _map_status_to_exception


@pytest.mark.parametrize(
    "status, exc_type",
    [
        (401, AuthenticationError),
        (403, PermissionDeniedError),
        (404, NotFoundError),
        (409, ConflictError),
        (422, ValidationError),
        (429, RateLimitError),
        (500, InternalServerError),
        (502, InternalServerError),
        (503, InternalServerError),
        (504, InternalServerError),
        (418, APIStatusError),  # unmapped status falls back to base
    ],
)
def test_status_codes_map_to_typed_exceptions(status, exc_type):
    exc = _map_status_to_exception(status, b'{"detail": "boom"}')
    assert isinstance(exc, exc_type)
    assert exc.status_code == status
    assert exc.message == "boom"


def test_non_json_body_is_preserved_in_message():
    exc = _map_status_to_exception(503, b"<html>maintenance</html>")
    assert isinstance(exc, InternalServerError)
    assert "maintenance" in exc.message


def test_validation_error_list_detail_is_joined():
    exc = _map_status_to_exception(422, b'{"detail": [{"msg": "field required"}, {"msg": "bad"}]}')
    assert isinstance(exc, ValidationError)
    assert "field required" in exc.message


def test_unified_envelope_422_prefers_error_over_list_detail():
    """The aethex unified 422 envelope carries both a human ``error`` sentence and a
    list-shaped ``detail``. The message must surface the readable ``error``, not a dump
    of the ``detail`` list."""
    exc = _map_status_to_exception(
        422,
        b'{"error": "Validation failed", "code": "validation_error", '
        b'"request_id": "req_123", "detail": [{"msg": "field required"}]}',
    )
    assert isinstance(exc, ValidationError)
    assert exc.message == "Validation failed"


def test_rate_limit_retry_after_from_header():
    exc = _map_status_to_exception(429, b'{"detail": "slow down"}', headers={"retry-after": "5.0"})
    assert isinstance(exc, RateLimitError)
    assert exc.retry_after == 5.0


def _make_response(status: int, body: bytes = b"{}"):
    """Build a minimal stand-in for the generated ``Response`` type."""
    return SimpleNamespace(
        status_code=status,
        content=body,
        headers={},
        parsed={"ok": True} if 200 <= status < 300 else None,
    )


def _stub_op(status: int, body: bytes = b"{}"):
    """Return a function with the same call shape as a generated `_detailed` op."""

    def _impl(*args, **kwargs):
        return _make_response(status, body)

    return _impl


def test_aethex_call_returns_parsed_on_2xx():
    client = AethexAI(api_key="ae_live_dummy", base_url="https://example.com")
    result = client._call(_stub_op(200, b'{"ok": true}'))
    assert result == {"ok": True}
    client.close()


def test_aethex_call_raises_on_401():
    client = AethexAI(api_key="ae_live_dummy", base_url="https://example.com")
    with pytest.raises(AuthenticationError) as info:
        client._call(_stub_op(401, b'{"detail": "bad key"}'))
    assert info.value.status_code == 401
    client.close()


def test_kora_call_raises_on_404():
    kora = Kora("https://example.com", "ae_live_dummy")
    with pytest.raises(NotFoundError):
        kora._call(_stub_op(404, b'{"detail": "missing"}'))
    kora.close()


def test_async_call_raises_on_500():
    async def _run():
        client = AsyncAethexAI(api_key="ae_live_dummy", base_url="https://example.com")
        try:

            async def _async_op(*args, **kwargs):
                return _make_response(500, b'{"detail": "boom"}')

            with pytest.raises(InternalServerError):
                await client._call(_async_op)
        finally:
            await client.close()

    asyncio.run(_run())
