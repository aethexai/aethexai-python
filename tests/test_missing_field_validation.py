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


def test_missing_single_field_raises_validation_error(sync_client: AethexAI) -> None:
    """Missing one required field surfaces as typed ValidationError naming the field."""
    with pytest.raises(ValidationError) as exc_info:
        sync_client.preview_voice()
    err = exc_info.value
    assert err.code == "missing_fields"
    assert err.status_code == 422
    assert err.response.get("missing_fields") == ["voice_id"]
    assert "voice_id" in err.message


def test_missing_multiple_fields_lists_all(sync_client: AethexAI) -> None:
    """All missing required fields are reported, not just the first one.

    ``presign_upload`` requires both ``content_type`` and ``kind``. Pre-fix the
    SDK raised ``KeyError('content_type')`` and dropped ``kind`` on the floor;
    we now mirror the server's 422 envelope which lists every missing field.
    """
    with pytest.raises(ValidationError) as exc_info:
        sync_client.presign_upload()
    missing = exc_info.value.response.get("missing_fields")
    assert missing == ["content_type", "kind"]


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
    missing = exc_info.value.response.get("missing_fields")
    # AgentCreate requires name, system_prompt, voice_id (order from attrs.fields).
    assert set(missing) == {"name", "system_prompt", "voice_id"}


def test_partial_kwargs_still_reports_remaining(sync_client: AethexAI) -> None:
    with pytest.raises(ValidationError) as exc_info:
        sync_client.create_agent(name="Bot")
    missing = exc_info.value.response.get("missing_fields")
    assert "name" not in missing
    assert set(missing) == {"system_prompt", "voice_id"}


async def test_async_client_also_raises_validation_error(
    async_client: AsyncAethexAI,
) -> None:
    """Parity: async wrappers raise the same typed error before the wire call."""
    with pytest.raises(ValidationError) as exc_info:
        await async_client.preview_voice()
    assert exc_info.value.response.get("missing_fields") == ["voice_id"]
