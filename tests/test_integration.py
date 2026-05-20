"""Optional live-API integration tests against ``dev-api.aethexai.com``.

These are gated on the ``AETHEX_API_KEY`` environment variable; without
it, every test in this file is skipped. They are also marked with the
``integration`` marker so they can be excluded from a fast unit-test run
via ``pytest -m "not integration"``.

The tests are intentionally minimal: they verify wire-level connectivity,
auth, and the most basic happy-path of two endpoints. They do not assert
deeply on payload shape because the dev environment's contents change.
"""

from __future__ import annotations

import os

import pytest

from aethexai import AethexAI, AuthenticationError, Kora

pytestmark = [
    pytest.mark.skipif(
        not os.getenv("AETHEX_API_KEY"),
        reason="set AETHEX_API_KEY to run integration tests",
    ),
    pytest.mark.integration,
]

DEV_BASE_URL = "https://dev-api.aethexai.com"


@pytest.fixture
def api_key() -> str:
    return os.environ["AETHEX_API_KEY"]


def test_kora_list_voices_returns_non_empty(api_key: str) -> None:
    kora = Kora(DEV_BASE_URL, api_key)
    try:
        voices = kora.list_voices()
        assert isinstance(voices, list)
        assert len(voices) > 0, "dev should always have at least one voice"
        # Sanity-check the response model rather than asserting on names.
        first = voices[0]
        assert getattr(first, "id", None), "voice.id should be populated"
    finally:
        kora.close()


def test_aethex_list_agents_returns_paginated(api_key: str) -> None:
    client = AethexAI(api_key=api_key, base_url=DEV_BASE_URL)
    try:
        page = client.list_agents()
        # PaginatedResponse always carries a .data list (possibly empty).
        assert hasattr(page, "data")
        assert isinstance(page.data, list)
    finally:
        client.close()


def test_kora_invalid_api_key_raises_authentication_error() -> None:
    kora = Kora(DEV_BASE_URL, "ae_live_dummy_does_not_exist")
    try:
        with pytest.raises(AuthenticationError) as info:
            kora.list_voices()
        assert info.value.status_code == 401
    finally:
        kora.close()


def test_aethex_get_usage_summary_smoke(api_key: str) -> None:
    """Smoke test for an endpoint that returns the tenant's usage roll-up."""
    client = AethexAI(api_key=api_key, base_url=DEV_BASE_URL)
    try:
        result = client.get_usage_summary()
        # Just verify we got something back without an exception.
        assert result is not None
    finally:
        client.close()
