"""Client-side validation of required body fields (AET-1524).

The previous behaviour was that omitting a required field on a POST wrapper
crashed with stdlib ``KeyError('field')`` from the generated
``*Create.from_dict()`` (calling ``d.pop("field")``). The wrapper built a
partial dict, the request never went out, and the user saw only the first
missing field.

These tests pin the new behaviour: a typed :class:`aethexai.ValidationError`
is raised before the wire call, listing every missing field.
"""

from __future__ import annotations

import pytest

from aethexai import AethexAI, AsyncAethexAI, ValidationError


@pytest.fixture
def sync_client() -> AethexAI:
    return AethexAI(api_key="ak_test_dummy", base_url="https://dev-api.aethexai.com")


@pytest.fixture
def async_client() -> AsyncAethexAI:
    return AsyncAethexAI(api_key="ak_test_dummy", base_url="https://dev-api.aethexai.com")


def _missing_fields(err: ValidationError) -> set[str]:
    """Extract the set of missing field names from the structured envelope.

    The pre-flight envelope mirrors the server's 422 shape: ``response["detail"]``
    is a list of ``{"type": "missing", "loc": ["body", <field>], ...}`` entries.
    """
    detail = err.response.get("detail", [])
    return {entry["loc"][1] for entry in detail if entry.get("type") == "missing"}


def test_missing_single_field_raises_validation_error(sync_client: AethexAI) -> None:
    """Missing one required field surfaces as typed ValidationError naming the field."""
    with pytest.raises(ValidationError) as exc_info:
        sync_client.preview_voice()
    err = exc_info.value
    assert err.code == "validation_error"
    assert err.status_code == 422
    assert _missing_fields(err) == {"voice_id"}
    assert "voice_id" in err.message


def test_missing_multiple_fields_lists_all(sync_client: AethexAI) -> None:
    """All missing required fields are reported, not just the first one.

    ``presign_upload`` requires both ``content_type`` and ``kind``. Pre-fix the
    SDK raised ``KeyError('content_type')`` and dropped ``kind`` on the floor;
    we now mirror the server's 422 envelope which lists every missing field.
    """
    with pytest.raises(ValidationError) as exc_info:
        sync_client.presign_upload()
    assert _missing_fields(exc_info.value) == {"content_type", "kind"}


def test_not_keyerror(sync_client: AethexAI) -> None:
    """The raised exception is aethexai.ValidationError, not stdlib KeyError."""
    with pytest.raises(ValidationError):
        sync_client.create_agent()
    # And specifically: catching KeyError must not catch this.
    try:
        sync_client.create_agent()
    except KeyError:  # pragma: no cover - regression guard
        pytest.fail("create_agent raised KeyError; expected ValidationError")
    except ValidationError:
        pass


def test_create_agent_lists_all_missing(sync_client: AethexAI) -> None:
    with pytest.raises(ValidationError) as exc_info:
        sync_client.create_agent()
    # AgentCreate requires name, system_prompt, voice_id.
    assert _missing_fields(exc_info.value) == {"name", "system_prompt", "voice_id"}


def test_partial_kwargs_still_reports_remaining(sync_client: AethexAI) -> None:
    with pytest.raises(ValidationError) as exc_info:
        sync_client.create_agent(name="Bot")
    missing = _missing_fields(exc_info.value)
    assert "name" not in missing
    assert missing == {"system_prompt", "voice_id"}


def test_envelope_matches_server_shape(sync_client: AethexAI) -> None:
    """Pre-flight envelope mirrors the server's 422 so one handler covers both paths.

    Server emits ``code="validation_error"``, ``detail=[{type,loc,msg,input}, ...]``
    with ``fields`` mirroring ``detail``. The pre-flight path emits the same shape
    so callers can write a single ``except ValidationError`` handler that iterates
    ``e.response["detail"]`` regardless of origin.
    """
    with pytest.raises(ValidationError) as exc_info:
        sync_client.create_agent()
    err = exc_info.value
    assert err.code == "validation_error"
    assert err.response["code"] == "validation_error"
    assert err.response["error"] == "Validation failed"
    assert err.response["request_id"] is None
    detail = err.response["detail"]
    assert isinstance(detail, list)
    assert err.response["fields"] == detail
    for entry in detail:
        assert entry["type"] == "missing"
        assert entry["loc"][0] == "body"
        assert entry["msg"] == "Field required"
        assert "input" in entry


async def test_async_client_also_raises_validation_error(
    async_client: AsyncAethexAI,
) -> None:
    """Parity: async wrappers raise the same typed error before the wire call."""
    with pytest.raises(ValidationError) as exc_info:
        await async_client.preview_voice()
    assert _missing_fields(exc_info.value) == {"voice_id"}
