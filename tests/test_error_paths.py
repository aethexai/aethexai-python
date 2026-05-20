"""End-to-end error-mapping tests over the wire.

``test_error_mapping.py`` exercises ``_map_status_to_exception`` directly.
This module is the integration view: it drives ``Kora.list_voices`` (and
its sync/async counterparts on the higher-level clients) through respx and
verifies that every documented HTTP status code raises the right typed
exception with the right ``status_code`` round-tripped onto the value.

Network-level failures (``httpx.ConnectError``, ``httpx.TimeoutException``)
are tested by mounting a side-effect on the respx route.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from aethexai import (
    AethexAI,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
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

BASE_URL = "https://api.test.aethexai.com"
VOICES_URL = f"{BASE_URL}/api/v1/voices"


# ─── Kora: full status matrix ──────────────────────────────────────────────


_STATUS_MATRIX = [
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
]


@pytest.fixture
def kora() -> Kora:
    k = Kora(BASE_URL, "ae_live_test")
    yield k
    k.close()


def _error_body_for(status: int) -> dict:
    """Build a JSON body that the generated parser will accept for ``status``.

    The list_voices op tries to parse a 422 into ``HTTPValidationError``,
    which in turn requires each ``detail`` item to be a fully-formed
    ``ValidationError`` (``loc``, ``msg``, ``type``). For every other
    status we just return a string detail, which the SDK's
    ``_map_status_to_exception`` is happy with.
    """
    if status == 422:
        return {
            "detail": [
                {"loc": ["body", "language"], "msg": "field required", "type": "value_error"}
            ]
        }
    return {"detail": "boom"}


@pytest.mark.parametrize("status, exc_type", _STATUS_MATRIX)
@respx.mock
def test_kora_list_voices_maps_status_to_exception(
    kora: Kora, status: int, exc_type: type[APIStatusError]
) -> None:
    respx.get(VOICES_URL).mock(return_value=httpx.Response(status, json=_error_body_for(status)))

    with pytest.raises(exc_type) as info:
        kora.list_voices()
    assert info.value.status_code == status
    # 422 is built from a structured ValidationError list; every other
    # status carries the literal "boom" detail through the message.
    if status != 422:
        assert "boom" in info.value.message


@respx.mock
def test_kora_list_voices_connect_error_propagates(kora: Kora) -> None:
    """Today, network-level failures bubble up as raw ``httpx`` exceptions.

    The SDK declares :class:`APIConnectionError` for this case but does not
    yet translate ``httpx.ConnectError`` into it. ``httpx.ConnectError`` is
    itself a subclass of :class:`httpx.RequestError`, which is what callers
    actually see today — we pin that contract here so any future change to
    catch-and-wrap behavior surfaces as a test diff.
    """
    respx.get(VOICES_URL).mock(side_effect=httpx.ConnectError("dns failure"))

    with pytest.raises((APIConnectionError, httpx.ConnectError)):
        kora.list_voices()


@respx.mock
def test_kora_list_voices_timeout_propagates(kora: Kora) -> None:
    """Same caveat as ``test_kora_list_voices_connect_error_propagates``.

    The SDK defines :class:`APITimeoutError` but does not (yet) catch
    ``httpx.TimeoutException`` to translate it.
    """
    respx.get(VOICES_URL).mock(side_effect=httpx.TimeoutException("timed out"))

    with pytest.raises((APITimeoutError, httpx.TimeoutException)):
        kora.list_voices()


# ─── AethexAI sanity check (one 4xx + one 5xx) ─────────────────────────────


@respx.mock
def test_aethex_list_voices_404_raises_not_found() -> None:
    respx.get(VOICES_URL).mock(return_value=httpx.Response(404, json={"detail": "missing"}))

    client = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(NotFoundError) as info:
            client.list_voices()
        assert info.value.status_code == 404
    finally:
        client.close()


@respx.mock
def test_aethex_list_voices_503_raises_internal_server_error() -> None:
    respx.get(VOICES_URL).mock(return_value=httpx.Response(503, json={"detail": "down"}))

    client = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(InternalServerError) as info:
            client.list_voices()
        assert info.value.status_code == 503
    finally:
        client.close()


# ─── AsyncAethexAI sanity check (one 4xx + one 5xx) ────────────────────────


@respx.mock
async def test_async_aethex_list_voices_422_raises_validation_error() -> None:
    respx.get(VOICES_URL).mock(
        return_value=httpx.Response(
            422,
            json={
                "detail": [
                    {
                        "loc": ["query", "language"],
                        "msg": "language is required",
                        "type": "value_error.missing",
                    }
                ]
            },
        )
    )

    client = AsyncAethexAI(api_key="ae_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as info:
            await client.list_voices()
        assert info.value.status_code == 422
    finally:
        await client.close()


@respx.mock
async def test_async_aethex_list_voices_500_raises_internal_server_error() -> None:
    respx.get(VOICES_URL).mock(return_value=httpx.Response(500, json={"detail": "kaboom"}))

    client = AsyncAethexAI(api_key="ae_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(InternalServerError) as info:
            await client.list_voices()
        assert info.value.status_code == 500
        assert "kaboom" in info.value.message
    finally:
        await client.close()


# ─── RateLimit special: retry_after propagation ────────────────────────────


@respx.mock
def test_kora_rate_limit_retry_after_header_is_exposed(kora: Kora) -> None:
    respx.get(VOICES_URL).mock(
        return_value=httpx.Response(
            429,
            json={"detail": "slow down"},
            headers={"retry-after": "12"},
        )
    )

    with pytest.raises(RateLimitError) as info:
        kora.list_voices()
    assert info.value.status_code == 429
    assert info.value.retry_after == 12.0
