"""AET-1631#7: a whitespace-only api_key is rejected at construction.

These tests exercise the constructor input-validation contract — no HTTP is
ever issued, so they need no respx / network mock. ``AETHEX_API_KEY`` is
removed from the environment so a stray env var can't satisfy the check.

Contracts under test:
  - AethexAI / AsyncAethexAI raise AuthenticationError(status_code=401) for an
    empty-or-whitespace api_key (same as an empty one).
  - Kora intentionally raises a stdlib ValueError ("api_key is required"),
    NOT AuthenticationError — that contract is preserved deliberately.
"""

import pytest

from aethexai import AethexAI, AsyncAethexAI, AuthenticationError, Kora

BASE_URL = "https://api.test.aethexai.com"


@pytest.fixture(autouse=True)
def _no_env_key(monkeypatch):
    """Ensure no AETHEX_API_KEY env var interferes with the constructor check."""
    monkeypatch.delenv("AETHEX_API_KEY", raising=False)


# --- AethexAI (sync) ---------------------------------------------------------


@pytest.mark.parametrize("blank", ["   ", "\t\n "])
def test_aethexai_whitespace_key_raises_auth_error(blank):
    with pytest.raises(AuthenticationError) as exc_info:
        AethexAI(api_key=blank, base_url=BASE_URL)
    assert exc_info.value.status_code == 401


# --- AsyncAethexAI -----------------------------------------------------------


@pytest.mark.parametrize("blank", ["   ", "\t\n "])
def test_async_aethexai_whitespace_key_raises_auth_error(blank):
    with pytest.raises(AuthenticationError) as exc_info:
        AsyncAethexAI(api_key=blank, base_url=BASE_URL)
    assert exc_info.value.status_code == 401


# --- Kora --------------------------------------------------------------------


@pytest.mark.parametrize("blank", ["   ", "\t\n "])
def test_kora_whitespace_key_raises_value_error(blank):
    # Kora deliberately raises a stdlib ValueError, NOT AuthenticationError.
    with pytest.raises(ValueError) as exc_info:
        Kora(BASE_URL, blank)
    assert "api_key is required" in str(exc_info.value)
    # Guard the contract: it must NOT be the typed AuthenticationError.
    assert not isinstance(exc_info.value, AuthenticationError)


# --- Positive controls -------------------------------------------------------


def test_aethexai_valid_key_constructs():
    client = AethexAI(api_key="ak_live_x", base_url=BASE_URL)
    try:
        assert client is not None
    finally:
        client.close()


def test_kora_valid_key_constructs():
    client = Kora(BASE_URL, "ak_live_x")
    try:
        assert client is not None
    finally:
        client.close()
