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


# ─── AET-1523: 422 must accept the aethex unified envelope ─────────────────


_AETHEX_422_ENVELOPE = {
    "error": "Invalid upload_id",
    "code": "validation_error",
    "request_id": "042f6f8d-1234-4d56-9abc-cafef00dbabe",
    "detail": "Invalid upload_id",
}


@respx.mock
def test_kora_422_aethex_envelope_raises_typed_validation_error(kora: Kora) -> None:
    """Regression: prior to AET-1523, a 422 with the aethex envelope crashed
    inside ``HTTPValidationError.from_dict`` with
    ``ValueError: dictionary update sequence element #0 has length 1; 2 is required``
    instead of raising the documented ``aethexai.ValidationError``.
    """
    respx.get(VOICES_URL).mock(return_value=httpx.Response(422, json=_AETHEX_422_ENVELOPE))

    with pytest.raises(ValidationError) as info:
        kora.list_voices()
    exc = info.value
    assert exc.status_code == 422
    assert exc.code == "validation_error"
    assert exc.message == "Invalid upload_id"
    assert "Invalid upload_id" in str(exc)
    assert exc.response == _AETHEX_422_ENVELOPE


@respx.mock
def test_aethex_422_aethex_envelope_raises_typed_validation_error() -> None:
    """Same regression, exercised through the high-level ``AethexAI`` wrapper."""
    respx.get(VOICES_URL).mock(return_value=httpx.Response(422, json=_AETHEX_422_ENVELOPE))

    client = AethexAI(api_key="ae_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as info:
            client.list_voices()
        exc = info.value
        assert exc.status_code == 422
        assert exc.code == "validation_error"
        assert exc.message == "Invalid upload_id"
        assert exc.response["request_id"] == _AETHEX_422_ENVELOPE["request_id"]
    finally:
        client.close()


@respx.mock
async def test_async_aethex_422_aethex_envelope_raises_typed_validation_error() -> None:
    """Same regression on the async client."""
    respx.get(VOICES_URL).mock(return_value=httpx.Response(422, json=_AETHEX_422_ENVELOPE))

    client = AsyncAethexAI(api_key="ae_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as info:
            await client.list_voices()
        exc = info.value
        assert exc.status_code == 422
        assert exc.code == "validation_error"
        assert exc.message == "Invalid upload_id"
    finally:
        await client.close()


def test_http_validation_error_from_dict_tolerates_aethex_envelope() -> None:
    """Unit-level guard on the generated ``from_dict`` patch.

    The OpenAPI spec types ``detail`` as ``list[ValidationError]``; the real
    API returns a string. ``from_dict`` must not raise — it should leave the
    typed ``detail`` field as UNSET and preserve the raw envelope in
    ``additional_properties`` so the wrapper layer can build the proper
    typed exception from ``response.content``.
    """
    from aethexai._generated.models.http_validation_error import HTTPValidationError
    from aethexai._generated.types import UNSET

    parsed = HTTPValidationError.from_dict(_AETHEX_422_ENVELOPE)
    assert parsed.detail is UNSET
    assert parsed.additional_properties["detail"] == "Invalid upload_id"
    assert parsed.additional_properties["code"] == "validation_error"
    assert parsed.additional_properties["error"] == "Invalid upload_id"


def test_http_validation_error_from_dict_still_parses_fastapi_shape() -> None:
    """The FastAPI-shaped ``detail`` (list of ValidationError dicts) must
    continue to parse — we only fall back when the list/items don't match.
    """
    from aethexai._generated.models.http_validation_error import HTTPValidationError

    payload = {
        "detail": [{"loc": ["body", "language"], "msg": "field required", "type": "value_error"}]
    }
    parsed = HTTPValidationError.from_dict(payload)
    assert isinstance(parsed.detail, list)
    assert len(parsed.detail) == 1
    assert parsed.detail[0].msg == "field required"
