"""Regression tests: the raw API key must never be exposed.

The raw API key must never appear in ``repr()`` / ``str(vars(...))`` /
exception messages on any of the three SDK clients. The fix has two parts:

1. The generated ``AuthenticatedClient.token`` and ``_headers`` fields are
   marked ``repr=False`` in the generated client.
2. ``AethexAI`` / ``AsyncAethexAI`` / ``Kora`` no longer store the raw key
   as ``self._api_key`` (it lives only inside ``self._client``).

If either side regresses, the assertions below catch it.
"""

from __future__ import annotations

import re

import httpx
import pytest
import respx

from aethexai import (
    AethexAI,
    AsyncAethexAI,
    AuthenticationError,
    Kora,
)
from aethexai._generated.client import _SECRET_FIELDS_PATCHED, AuthenticatedClient

_SECRET = "ae_live_supersecret_dummy_for_test_0123456789abcdef"
_KEY_PATTERN = re.compile(r"ae_live_[a-zA-Z0-9_-]+|ak_live_[a-zA-Z0-9_-]+")


def _assert_no_key(haystack: str, label: str) -> None:
    assert _SECRET not in haystack, f"{label} leaked the raw API key: {haystack[:300]}"
    match = _KEY_PATTERN.search(haystack)
    assert match is None, (
        f"{label} leaked an API-key-shaped substring {match.group(0)!r}: {haystack[:300]}"
    )


def test_codegen_sentinel_present() -> None:
    """If the codegen sentinel is missing, regeneration has wiped the patch."""
    assert _SECRET_FIELDS_PATCHED is True


# ── AethexAI ─────────────────────────────────────────────────────────────


def test_aethexai_repr_does_not_leak_key() -> None:
    c = AethexAI(api_key=_SECRET, base_url="https://x.example")
    try:
        _assert_no_key(repr(c), "repr(AethexAI)")
        _assert_no_key(str(c), "str(AethexAI)")
    finally:
        c.close()


def test_aethexai_vars_does_not_leak_key() -> None:
    c = AethexAI(api_key=_SECRET, base_url="https://x.example")
    try:
        _assert_no_key(str(vars(c)), "str(vars(AethexAI))")
        _assert_no_key(str(c.__dict__), "AethexAI.__dict__")
    finally:
        c.close()


def test_aethexai_inner_client_repr_does_not_leak_key() -> None:
    c = AethexAI(api_key=_SECRET, base_url="https://x.example")
    try:
        _assert_no_key(repr(c._client), "repr(AethexAI._client)")
    finally:
        c.close()


def test_aethexai_inner_client_repr_does_not_leak_after_lazy_init() -> None:
    """Lazy ``get_httpx_client()`` writes the auth header into ``_headers``.

    If ``_headers`` were ever repr'd, the API key would leak from there too.
    """
    c = AethexAI(api_key=_SECRET, base_url="https://x.example")
    try:
        # Force the lazy init so _headers is populated with the auth header.
        c._client.get_httpx_client()
        _assert_no_key(repr(c._client), "repr(AethexAI._client) post-lazy-init")
    finally:
        c.close()


# ── AsyncAethexAI ────────────────────────────────────────────────────────


async def test_async_repr_does_not_leak_key() -> None:
    c = AsyncAethexAI(api_key=_SECRET, base_url="https://x.example")
    try:
        _assert_no_key(repr(c), "repr(AsyncAethexAI)")
        _assert_no_key(str(vars(c)), "str(vars(AsyncAethexAI))")
        _assert_no_key(repr(c._client), "repr(AsyncAethexAI._client)")
    finally:
        await c.close()


# ── Kora ─────────────────────────────────────────────────────────────────


def test_kora_repr_does_not_leak_key() -> None:
    c = Kora(base_url="https://x.example", api_key=_SECRET)
    try:
        _assert_no_key(repr(c), "repr(Kora)")
        _assert_no_key(str(vars(c)), "str(vars(Kora))")
        _assert_no_key(repr(c._client), "repr(Kora._client)")
    finally:
        c.close()


# ── Exception paths ──────────────────────────────────────────────────────


@respx.mock
def test_aethexai_exception_message_does_not_leak_key() -> None:
    """A 401 from the server must not echo the key back through our exception."""
    base = "https://x.example"
    respx.get(f"{base}/api/v1/voices").respond(401, json={"detail": "Invalid API key"})
    c = AethexAI(api_key=_SECRET, base_url=base)
    try:
        with pytest.raises(AuthenticationError) as excinfo:
            c.list_voices(limit=1)
        # Both the message and the repr of the exception must be clean.
        _assert_no_key(str(excinfo.value), "AuthenticationError str")
        _assert_no_key(repr(excinfo.value), "AuthenticationError repr")
    finally:
        c.close()


@respx.mock
def test_aethexai_connection_error_does_not_leak_key() -> None:
    """A network error must not leak the key via the wrapped httpx exception."""
    base = "https://x.example"
    respx.get(f"{base}/api/v1/voices").mock(side_effect=httpx.ConnectError("boom"))
    c = AethexAI(api_key=_SECRET, base_url=base)
    try:
        with pytest.raises(Exception) as excinfo:
            c.list_voices(limit=1)
        _assert_no_key(str(excinfo.value), "ConnectionError str")
        _assert_no_key(repr(excinfo.value), "ConnectionError repr")
        if excinfo.value.__cause__ is not None:
            _assert_no_key(str(excinfo.value.__cause__), "ConnectionError __cause__ str")
            _assert_no_key(repr(excinfo.value.__cause__), "ConnectionError __cause__ repr")
    finally:
        c.close()


# ── Sanity: token still actually works ──────────────────────────────────


@respx.mock
def test_aethexai_still_sends_x_api_key_header() -> None:
    """Suppressing token from repr must NOT suppress it from the auth header."""
    base = "https://x.example"
    route = respx.get(f"{base}/api/v1/voices").respond(200, json=[])
    c = AethexAI(api_key=_SECRET, base_url=base)
    try:
        c.list_voices(limit=1)
        # Capture the actual request that went out.
        assert route.called, "list_voices did not hit the mocked route"
        sent = route.calls[0].request
        assert sent.headers.get("X-API-Key") == _SECRET, (
            "X-API-Key header must still carry the raw token even though "
            "repr() does not — anything else means we broke auth"
        )
    finally:
        c.close()


def test_authenticated_client_token_field_is_repr_false() -> None:
    """Belt-and-braces: introspect the attrs field metadata directly.

    If a future refactor swaps the post-codegen patch for a subclass approach
    and forgets to suppress the field on the parent, this fails.
    """
    import attrs

    field_names_in_repr = {f.name for f in attrs.fields(AuthenticatedClient) if f.repr is not False}
    assert "token" not in field_names_in_repr, (
        "AuthenticatedClient.token must be repr=False — otherwise the raw "
        "API key appears in every default __repr__"
    )
    assert "_headers" not in field_names_in_repr, (
        "AuthenticatedClient._headers must be repr=False — the auth header "
        "value gets written into it by get_httpx_client()"
    )
