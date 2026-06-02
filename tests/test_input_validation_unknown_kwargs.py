"""Unknown body kwargs are rejected with a typed ValidationError (AET-1632).

Pre-fix, an unrecognized body field was silently absorbed into the generated
model's ``additional_properties`` and dropped on the floor — a typo'd kwarg
(e.g. ``resorce_type=``) failed silently with no server-side effect. Now
:func:`aethexai._body.build_body` rejects unknown keys with a typed
:class:`aethexai.ValidationError` that names the offending key, *before* any
HTTP call.

The one deliberate exception is ``create_agent`` / ``update_agent``, which pass
``allow_extra=True`` to preserve forward-compat tolerance: a newer server field
passed by an older SDK must not hard-fail.

These tests need no network mock: the rejection happens before the wire call.
"""

from __future__ import annotations

import pytest

from aethexai import AethexAI, ValidationError
from aethexai._body import build_body
from aethexai._generated.models.agent_create import AgentCreate
from aethexai._generated.models.usage_trigger_create import UsageTriggerCreate

BASE_URL = "https://api.test.aethexai.com"

# UsageTriggerCreate required (no-default) wire fields: event_callback_url,
# resource_type, threshold_value. period/threshold_type carry defaults.
VALID_TRIGGER_FIELDS = {
    "event_callback_url": "https://example.com/hook",
    "resource_type": "calls",
    "threshold_value": 100,
}


def _detail_keys(err: ValidationError) -> set[str]:
    """Extract the body field names from the structured 422 envelope."""
    detail = err.response.get("detail", [])
    return {entry["loc"][1] for entry in detail if len(entry.get("loc", [])) > 1}


# --- build_body unit level --------------------------------------------------


def test_build_body_rejects_unknown_key() -> None:
    """An unrecognized key raises a typed ValidationError naming the key."""
    with pytest.raises(ValidationError) as exc_info:
        build_body(
            UsageTriggerCreate,
            {**VALID_TRIGGER_FIELDS, "totally_unknown_field": 1},
        )
    err = exc_info.value
    assert err.status_code == 422
    assert err.code == "validation_error"
    # The offending key is surfaced — in the message and the envelope detail.
    assert "totally_unknown_field" in str(err)
    assert "totally_unknown_field" in _detail_keys(err)


def test_build_body_unknown_key_is_not_stdlib_error() -> None:
    """The rejection is a typed ValidationError, not a bare ValueError/TypeError."""
    try:
        build_body(
            UsageTriggerCreate,
            {**VALID_TRIGGER_FIELDS, "totally_unknown_field": 1},
        )
    except ValidationError:
        pass
    except (ValueError, TypeError) as exc:  # pragma: no cover - regression guard
        pytest.fail(f"expected ValidationError, got stdlib {type(exc).__name__}: {exc}")
    else:  # pragma: no cover - regression guard
        pytest.fail("build_body did not raise on unknown key")


def test_build_body_valid_fields_do_not_raise() -> None:
    """A dict of only known fields constructs the model without error."""
    body = build_body(UsageTriggerCreate, dict(VALID_TRIGGER_FIELDS))
    assert isinstance(body, UsageTriggerCreate)
    assert body.event_callback_url == "https://example.com/hook"
    assert body.resource_type == "calls"
    assert body.threshold_value == 100


def test_build_body_known_optional_field_not_rejected() -> None:
    """Optional fields with defaults (period) are known keys, not 'unknown'."""
    body = build_body(
        UsageTriggerCreate,
        {**VALID_TRIGGER_FIELDS, "period": "daily"},
    )
    assert isinstance(body, UsageTriggerCreate)
    assert body.period == "daily"


# --- tolerance control: allow_extra=True ------------------------------------


def test_allow_extra_tolerates_unknown_key() -> None:
    """create_agent/update_agent pass allow_extra=True: forward-compat preserved.

    An unrecognized field must NOT hard-fail; it lands in additional_properties.
    """
    body = build_body(
        AgentCreate,
        {
            "name": "n",
            "system_prompt": "p",
            "voice_id": "v",
            "made_up_field": 1,
        },
        allow_extra=True,
    )
    assert isinstance(body, AgentCreate)
    assert body.name == "n"
    # The unknown field is tolerated and forwarded, not rejected.
    assert body.additional_properties.get("made_up_field") == 1


def test_default_rejects_what_allow_extra_tolerates() -> None:
    """Same unknown key on AgentCreate WITHOUT allow_extra is rejected.

    Confirms the difference is the flag, not the model.
    """
    with pytest.raises(ValidationError) as exc_info:
        build_body(
            AgentCreate,
            {
                "name": "n",
                "system_prompt": "p",
                "voice_id": "v",
                "made_up_field": 1,
            },
        )
    assert "made_up_field" in str(exc_info.value)


# --- wrapper level ----------------------------------------------------------


def test_create_trigger_rejects_bogus_kwarg() -> None:
    """The sync wrapper rejects an unknown kwarg before any HTTP call (no respx)."""
    client = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    try:
        with pytest.raises(ValidationError) as exc_info:
            client.create_trigger(**VALID_TRIGGER_FIELDS, bogus_kwarg=1)
        err = exc_info.value
        assert err.status_code == 422
        assert err.code == "validation_error"
        assert "bogus_kwarg" in str(err)
        assert "bogus_kwarg" in _detail_keys(err)
    finally:
        client.close()
