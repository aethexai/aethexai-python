"""Typed-error coercion for malformed BODY input (AET-1631 #1/#2/#4).

Pre-fix, a body value with the wrong *shape* (a list of bare phone strings
where the model wants ``[{"to_number": ...}]``, a malformed body UUID, a scalar
where a list is required) escaped as a bare stdlib ``ValueError`` / ``TypeError``
raised deep inside the generated ``*.from_dict`` coercion. A caller doing
``except aethexai.AethexError`` (or ``except aethexai.ValidationError``) would
miss it entirely.

These tests pin the new contract: :func:`aethexai._body.build_body` wraps
``from_dict`` so any coercion failure surfaces as a typed
:class:`aethexai.ValidationError` (``status_code=422``,
``code="validation_error"``) *before* any HTTP call goes out. No ``respx`` and
no network mock are needed: the error is raised pre-flight.

Each test asserts ``pytest.raises(ValidationError)`` and that the raised object
*is* a ``ValidationError`` — a bare stdlib ``ValueError`` / ``TypeError`` would
NOT match ``pytest.raises(ValidationError)``, which is the whole point of the
fix.
"""

from __future__ import annotations

import pytest

from aethexai import AethexAI, ValidationError

BASE_URL = "https://api.test.aethexai.com"

# A syntactically valid UUID, so the only bad value under test is the one each
# case is exercising (recipients shape / agent_id uuid / items type).
GOOD_AGENT_ID = "11111111-1111-1111-1111-111111111111"


@pytest.fixture
def client() -> AethexAI:
    c = AethexAI(api_key="ak_live_test", base_url=BASE_URL)
    yield c
    c.close()


def _assert_typed_validation_error(exc_info: pytest.ExceptionInfo[ValidationError]) -> None:
    """Assert the captured exception is the typed ValidationError contract.

    Note: ``pytest.raises(ValidationError)`` already guarantees a bare stdlib
    ``ValueError`` / ``TypeError`` could not have matched — that is the contract
    AET-1631 establishes. We additionally pin the typed envelope fields.
    """
    err = exc_info.value
    assert isinstance(err, ValidationError)
    # Belt-and-suspenders: a stdlib ValueError/TypeError is NOT a ValidationError.
    assert not isinstance(err, (ValueError, TypeError))
    assert err.status_code == 422
    assert err.code == "validation_error"
    assert isinstance(err.response, dict)
    assert isinstance(err.message, str)


def test_batch_calls_bare_phone_strings_raises_validation_error(client: AethexAI) -> None:
    """recipients=["+1555..."] (bare strings, not [{"to_number": ...}]) -> ValidationError.

    Pre-fix this raised a bare stdlib ValueError/TypeError from inside
    ``BatchCallCreate.from_dict`` while coercing each recipient dict, escaping any
    ``except ValidationError`` handler. agent_id is a valid UUID so the *only*
    malformed input is the recipients shape.
    """
    with pytest.raises(ValidationError) as exc_info:
        client.batch_calls(agent_id=GOOD_AGENT_ID, recipients=["+15551234567"])
    _assert_typed_validation_error(exc_info)


def test_conversation_connect_bad_uuid_raises_validation_error(client: AethexAI) -> None:
    """conversation_connect(agent_id="bad-uuid") -> ValidationError.

    Pre-fix the body UUID coercion in ``ConnectRequest.from_dict`` raised a bare
    stdlib ValueError ("badly formed hexadecimal UUID string"), not a typed error.
    """
    with pytest.raises(ValidationError) as exc_info:
        client.conversation_connect(agent_id="bad-uuid")
    _assert_typed_validation_error(exc_info)


def test_batch_synthesize_non_list_items_raises_validation_error(client: AethexAI) -> None:
    """batch_synthesize(items="notalist") -> ValidationError.

    Pre-fix, passing a scalar string where ``TTSBatchCreate`` expects a list of
    items raised a bare stdlib ValueError/TypeError during ``from_dict`` coercion
    instead of the typed error.
    """
    with pytest.raises(ValidationError) as exc_info:
        client.batch_synthesize(items="notalist")
    _assert_typed_validation_error(exc_info)


def test_bad_body_input_is_not_stdlib_valueerror(client: AethexAI) -> None:
    """Regression guard: the raised type is ValidationError, never a bare ValueError.

    Catching only ``ValueError`` / ``TypeError`` must NOT swallow these — that was
    the broken pre-fix behaviour. ``ValidationError`` does not subclass either, so
    this re-raises out of the narrow except and is caught as ValidationError.
    """
    try:
        client.conversation_connect(agent_id="bad-uuid")
    except (ValueError, TypeError):  # pragma: no cover - regression guard
        pytest.fail(
            "conversation_connect raised a stdlib ValueError/TypeError; expected ValidationError"
        )
    except ValidationError:
        pass
    else:  # pragma: no cover - the bad input must raise
        pytest.fail("conversation_connect did not raise on a malformed body UUID")
