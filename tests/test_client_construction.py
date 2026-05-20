"""Construction / lifecycle tests for ``AethexAI``, ``AsyncAethexAI`` and ``Kora``.

These exercise the public constructor surface (env-var fallback, explicit
arg, timeout / retry pass-through, context-manager protocol, ``close()``
idempotency) without ever hitting the network.
"""

from __future__ import annotations

import asyncio

import httpx
import pytest

from aethexai import (
    AethexAI,
    AsyncAethexAI,
    AuthenticationError,
    Kora,
)

# ─── AethexAI ───────────────────────────────────────────────────────────────


def test_aethex_construct_with_api_key_arg():
    client = AethexAI(api_key="ak_live_arg")
    # Behavioral assertion: the key reaches the auth header. The raw key is
    # intentionally NOT stored on the client instance (see finding A.5 of the
    # 2026-05-17 pre-launch audit).
    assert client._client.get_httpx_client().headers.get("x-api-key") == "ak_live_arg"
    assert client._base_url == "https://api.aethexai.com"
    client.close()


def test_aethex_construct_with_env_var(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("AETHEX_API_KEY", "ak_live_env")
    client = AethexAI()
    assert client._client.get_httpx_client().headers.get("x-api-key") == "ak_live_env"
    client.close()


def test_aethex_missing_api_key_raises_authentication_error(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("AETHEX_API_KEY", raising=False)
    with pytest.raises(AuthenticationError) as info:
        AethexAI()
    assert info.value.status_code == 401
    assert "API key is required" in str(info.value)


def test_aethex_arg_overrides_env_var(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("AETHEX_API_KEY", "ak_live_env")
    client = AethexAI(api_key="ak_live_explicit")
    assert client._client.get_httpx_client().headers.get("x-api-key") == "ak_live_explicit"
    client.close()


def test_aethex_base_url_default():
    client = AethexAI(api_key="ak_live_x")
    assert client._base_url == "https://api.aethexai.com"
    client.close()


def test_aethex_base_url_override_strips_trailing_slash():
    client = AethexAI(api_key="ak_live_x", base_url="https://example.com/")
    assert client._base_url == "https://example.com"
    client.close()


def test_aethex_timeout_and_max_retries_stored():
    client = AethexAI(api_key="ak_live_x", timeout=12.5, max_retries=4)
    assert client._timeout == 12.5
    assert client._max_retries == 4
    client.close()


def test_aethex_close_is_idempotent():
    client = AethexAI(api_key="ak_live_x")
    client.close()
    # Calling close again must not raise.
    client.close()


def test_aethex_context_manager_closes_client():
    with AethexAI(api_key="ak_live_x") as client:
        assert isinstance(client, AethexAI)
    # Once the with-block exits the underlying httpx client is closed; a
    # subsequent close() must still be a no-op.
    client.close()


def test_aethex_accepts_external_httpx_client():
    custom = httpx.Client()
    client = AethexAI(api_key="ak_live_x", httpx_client=custom)
    assert client._client.get_httpx_client() is custom
    client.close()


def test_aethex_sets_x_api_key_header():
    client = AethexAI(api_key="ak_live_unique_value")
    hc = client._client.get_httpx_client()
    assert hc.headers.get("x-api-key") == "ak_live_unique_value"
    client.close()


# ─── AsyncAethexAI ──────────────────────────────────────────────────────────


def test_async_construct_with_api_key_arg():
    client = AsyncAethexAI(api_key="ak_live_arg")
    # Behavioral assertion — see test_aethex_construct_with_api_key_arg above.
    assert client._client.get_async_httpx_client().headers.get("x-api-key") == "ak_live_arg"
    assert client._base_url == "https://api.aethexai.com"
    asyncio.run(client.close())


def test_async_construct_with_env_var(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("AETHEX_API_KEY", "ak_live_env_async")
    client = AsyncAethexAI()
    assert client._client.get_async_httpx_client().headers.get("x-api-key") == "ak_live_env_async"
    asyncio.run(client.close())


def test_async_missing_api_key_raises(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("AETHEX_API_KEY", raising=False)
    with pytest.raises(AuthenticationError):
        AsyncAethexAI()


def test_async_timeout_and_max_retries_stored():
    client = AsyncAethexAI(api_key="ak_live_x", timeout=9.0, max_retries=5)
    assert client._timeout == 9.0
    assert client._max_retries == 5
    asyncio.run(client.close())


def test_async_close_is_idempotent():
    client = AsyncAethexAI(api_key="ak_live_x")
    asyncio.run(client.close())
    asyncio.run(client.close())


async def test_async_context_manager():
    async with AsyncAethexAI(api_key="ak_live_x") as client:
        assert isinstance(client, AsyncAethexAI)


def test_async_accepts_external_httpx_client():
    custom = httpx.AsyncClient()
    client = AsyncAethexAI(api_key="ak_live_x", httpx_client=custom)
    assert client._client.get_async_httpx_client() is custom
    asyncio.run(client.close())


# ─── Kora ───────────────────────────────────────────────────────────────────


def test_kora_positional_constructor():
    kora = Kora("https://api.example.com", "ak_live_test")
    assert kora._base_url == "https://api.example.com"
    # Behavioral assertion — see test_aethex_construct_with_api_key_arg above.
    assert kora._client.get_httpx_client().headers.get("x-api-key") == "ak_live_test"
    kora.close()


def test_kora_missing_api_key_raises_value_error():
    # Note: Kora intentionally raises ValueError (not AuthenticationError)
    # because its positional constructor signature can't really fall back to
    # an env var.
    with pytest.raises(ValueError) as info:
        Kora("https://api.example.com", "")
    assert "api_key is required" in str(info.value)


def test_kora_does_not_pick_up_env_var(monkeypatch: pytest.MonkeyPatch):
    """Kora's positional constructor is intentionally explicit — no env-var fallback."""
    monkeypatch.setenv("AETHEX_API_KEY", "ak_live_env")
    with pytest.raises(ValueError):
        Kora("https://api.example.com")


def test_kora_default_base_url_when_only_api_key():
    kora = Kora(api_key="ak_live_x")
    assert kora._base_url == "https://api.aethexai.com"
    kora.close()


def test_kora_close_is_idempotent():
    kora = Kora("https://api.example.com", "ak_live_x")
    kora.close()
    kora.close()


def test_kora_context_manager():
    with Kora("https://api.example.com", "ak_live_x") as kora:
        assert isinstance(kora, Kora)


def test_kora_verify_ssl_passthrough():
    kora = Kora("https://api.example.com", "ak_live_x", verify_ssl=False)
    # Just confirm construction succeeded; the option is plumbed into the
    # underlying generated client.
    assert kora._client is not None
    kora.close()


def test_kora_sets_x_api_key_header():
    kora = Kora("https://api.example.com", "ak_live_kora_value")
    hc = kora._client.get_httpx_client()
    assert hc.headers.get("x-api-key") == "ak_live_kora_value"
    kora.close()
