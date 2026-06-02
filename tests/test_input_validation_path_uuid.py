"""Path-parameter UUID coercion raises a typed ValidationError (AET-1625 / AET-1631#6).

A malformed path-param UUID now raises :class:`aethexai.ValidationError`
*before* any HTTP call — not a stdlib ``ValueError``. These tests therefore
need NO respx and NO network mock: the error is raised synchronously inside the
wrapper while building the request. Asserting ``pytest.raises(ValidationError)``
is load-bearing — a bare ``ValueError`` would not match, which is the point.
"""

from __future__ import annotations

from uuid import UUID, uuid4

import pytest

from aethexai import AethexAI, AsyncAethexAI, Kora, ValidationError
from aethexai._body import coerce_uuid

BASE_URL = "https://api.test.aethexai.com"


def _assert_typed(exc: ValidationError) -> None:
    """Every path-UUID ValidationError carries the server-shaped 422 envelope."""
    assert exc.status_code == 422
    assert exc.code == "validation_error"
    assert isinstance(exc.response, dict)
    assert isinstance(exc.message, str)


# ---------------------------------------------------------------------------
# AethexAI (sync)
# ---------------------------------------------------------------------------


def test_sync_get_agent_bad_uuid_raises_validation_error() -> None:
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as ei:
            c.get_agent("bad-uuid")
        _assert_typed(ei.value)
    finally:
        c.close()


def test_sync_get_call_bad_uuid_raises_validation_error() -> None:
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as ei:
            c.get_call("bad-uuid")
        _assert_typed(ei.value)
    finally:
        c.close()


def test_sync_get_conversation_bad_uuid_raises_validation_error() -> None:
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as ei:
            c.get_conversation("not-a-uuid")
        _assert_typed(ei.value)
    finally:
        c.close()


def test_sync_get_recording_bad_uuid_raises_validation_error() -> None:
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as ei:
            c.get_recording("bad-uuid")
        _assert_typed(ei.value)
    finally:
        c.close()


def test_sync_get_transcription_job_bad_uuid_raises_validation_error() -> None:
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as ei:
            c.get_transcription_job("bad-uuid")
        _assert_typed(ei.value)
    finally:
        c.close()


# ---------------------------------------------------------------------------
# AsyncAethexAI
# ---------------------------------------------------------------------------


async def test_async_get_agent_bad_uuid_raises_validation_error() -> None:
    c = AsyncAethexAI(api_key="ak_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as ei:
            await c.get_agent("bad-uuid")
        _assert_typed(ei.value)
    finally:
        await c.close()


async def test_async_get_call_bad_uuid_raises_validation_error() -> None:
    c = AsyncAethexAI(api_key="ak_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as ei:
            await c.get_call("bad-uuid")
        _assert_typed(ei.value)
    finally:
        await c.close()


async def test_async_get_conversation_bad_uuid_raises_validation_error() -> None:
    c = AsyncAethexAI(api_key="ak_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as ei:
            await c.get_conversation("not-a-uuid")
        _assert_typed(ei.value)
    finally:
        await c.close()


# ---------------------------------------------------------------------------
# Kora
# ---------------------------------------------------------------------------


def test_kora_get_agent_bad_uuid_raises_validation_error() -> None:
    k = Kora(BASE_URL, "ae_live_test")
    try:
        with pytest.raises(ValidationError) as ei:
            k.get_agent("bad-uuid")
        _assert_typed(ei.value)
    finally:
        k.close()


def test_kora_get_call_bad_uuid_raises_validation_error() -> None:
    k = Kora(BASE_URL, "ae_live_test")
    try:
        with pytest.raises(ValidationError) as ei:
            k.get_call("bad-uuid")
        _assert_typed(ei.value)
    finally:
        k.close()


def test_kora_get_conversation_bad_uuid_raises_validation_error() -> None:
    k = Kora(BASE_URL, "ae_live_test")
    try:
        with pytest.raises(ValidationError) as ei:
            k.get_conversation("bad-uuid")
        _assert_typed(ei.value)
    finally:
        k.close()


def test_kora_delete_agent_bad_uuid_raises_validation_error() -> None:
    k = Kora(BASE_URL, "ae_live_test")
    try:
        with pytest.raises(ValidationError) as ei:
            k.delete_agent("bad-uuid")
        _assert_typed(ei.value)
    finally:
        k.close()


# ---------------------------------------------------------------------------
# Positive control: a syntactically valid uuid4() must NOT raise before HTTP.
# ---------------------------------------------------------------------------


def test_valid_uuid_does_not_raise_at_coercion() -> None:
    good = str(uuid4())
    result = coerce_uuid(good, "x")
    assert isinstance(result, UUID)
    assert str(result) == good
