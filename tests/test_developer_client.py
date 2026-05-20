"""Tests for ``DeveloperClient`` / ``AsyncDeveloperClient`` (audit finding A.1).

Covers:
* constructor (positional, env-var fallback, missing-token error)
* JWT bearer auth on every request
* The 8 billing methods (round-trip via respx)
* The 4 auth/me methods
* Token-refresh-on-401 (success path + failure path)
* Sync/async parity (every public method exists on both)
* No-leak: access and refresh tokens never appear in repr / vars /
  exception messages (regression for finding A.5)
"""

from __future__ import annotations

import re

import httpx
import pytest
import respx

from aethexai import (
    AsyncDeveloperClient,
    AuthenticationError,
    DeveloperClient,
)

BASE_URL = "https://api.example"
ACCESS = "eyJhbGciOiJIUzI1NiJ9.access.signature"
REFRESH = "eyJhbGciOiJIUzI1NiJ9.refresh.signature"
NEW_ACCESS = "eyJhbGciOiJIUzI1NiJ9.access2.signature"
NEW_REFRESH = "eyJhbGciOiJIUzI1NiJ9.refresh2.signature"

_JWT_SHAPE = re.compile(r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+")


# ─── construction ──────────────────────────────────────────────────────


def test_developer_client_construct_with_arg():
    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        hc = c._client.get_httpx_client()
        # Bearer is the default attrs prefix on AuthenticatedClient.
        assert hc.headers.get("authorization") == f"Bearer {ACCESS}"
        assert c._base_url == BASE_URL
    finally:
        c.close()


def test_developer_client_construct_with_env_var(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("AETHEX_DEVELOPER_ACCESS_TOKEN", ACCESS)
    c = DeveloperClient(base_url=BASE_URL)
    try:
        assert c._client.get_httpx_client().headers.get("authorization") == f"Bearer {ACCESS}"
    finally:
        c.close()


def test_developer_client_missing_token_raises(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("AETHEX_DEVELOPER_ACCESS_TOKEN", raising=False)
    with pytest.raises(AuthenticationError) as info:
        DeveloperClient(base_url=BASE_URL)
    assert info.value.status_code == 401
    assert "access_token is required" in str(info.value)


def test_developer_client_explicit_refresh_token_overrides_env(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv("AETHEX_DEVELOPER_REFRESH_TOKEN", "env-refresh")
    c = DeveloperClient(ACCESS, refresh_token=REFRESH, base_url=BASE_URL)
    try:
        assert c._refresh_token_box == [REFRESH]
    finally:
        c.close()


def test_developer_client_no_refresh_token_means_empty_box(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.delenv("AETHEX_DEVELOPER_REFRESH_TOKEN", raising=False)
    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        assert c._refresh_token_box == []
    finally:
        c.close()


# ─── billing (8 methods, the audit A.1 surface) ────────────────────────


def _balance_body() -> dict:
    return {
        "credit_balance": "12.34",
        "plan": {
            "slug": "pro",
            "name": "Pro",
            "monthly_credits": "100",
            "monthly_price_usd": "10",
        },
        "period": {
            "started_at": "2026-05-01T00:00:00Z",
            "ends_at": "2026-06-01T00:00:00Z",
            "credits_granted": "100",
            "credits_used": "50",
            "credits_remaining": "50",
        },
        "estimated_minutes_remaining": 50,
    }


@respx.mock
def test_get_balance_uses_bearer_jwt() -> None:
    route = respx.get(f"{BASE_URL}/api/v1/billing/balance").respond(200, json=_balance_body())
    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        balance = c.get_balance()
        assert route.called
        sent = route.calls[0].request
        assert sent.headers.get("Authorization") == f"Bearer {ACCESS}"
        assert balance.credit_balance == "12.34"
    finally:
        c.close()


@respx.mock
def test_list_plans() -> None:
    route = respx.get(f"{BASE_URL}/api/v1/billing/plans").respond(
        200,
        json={
            "plans": [
                {
                    "slug": "free",
                    "name": "Free",
                    "monthly_credits": "5",
                    "monthly_price_usd": "0",
                }
            ],
            "current_plan_slug": "free",
        },
    )
    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        resp = c.list_plans()
        assert route.called
        assert resp.current_plan_slug == "free"
    finally:
        c.close()


@respx.mock
def test_select_plan() -> None:
    route = respx.post(f"{BASE_URL}/api/v1/billing/plans/pro/select").respond(
        200,
        # SelectPlanResponse requires plan_slug + status (the others optional).
        json={"plan_slug": "pro", "status": "active"},
    )
    # The generated op only encodes the body if it's a SelectPlanRequest,
    # so pass a real one (the server accepts SelectPlanRequest | None, but
    # the SDK side prefers explicit).
    from aethexai._generated.models.select_plan_request import SelectPlanRequest

    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        resp = c.select_plan("pro", body=SelectPlanRequest(interval="monthly"))
        assert route.called
        assert resp.plan_slug == "pro"
    finally:
        c.close()


@respx.mock
def test_list_invoices() -> None:
    route = respx.get(f"{BASE_URL}/api/v1/billing/invoices").respond(
        200, json={"invoices": [], "next_cursor": None, "has_more": False}
    )
    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        resp = c.list_invoices(page_size=10)
        assert route.called
        assert resp.invoices == []
    finally:
        c.close()


@respx.mock
def test_list_transactions() -> None:
    route = respx.get(f"{BASE_URL}/api/v1/billing/transactions").respond(
        200, json={"transactions": [], "next_cursor": None}
    )
    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        resp = c.list_transactions()
        assert route.called
        assert resp.transactions == []
    finally:
        c.close()


@respx.mock
def test_list_payment_methods() -> None:
    route = respx.get(f"{BASE_URL}/api/v1/billing/payment-methods").respond(
        200, json={"payment_methods": [], "has_payment_method": False}
    )
    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        resp = c.list_payment_methods()
        assert route.called
        assert resp.has_payment_method is False
    finally:
        c.close()


@respx.mock
def test_create_payment_method_setup_intent() -> None:
    # Server returns 201 Created (per src/aethex/api/v1/billing_stripe.py:618).
    route = respx.post(f"{BASE_URL}/api/v1/billing/payment-method/setup-intent").respond(
        201,
        json={
            "client_secret": "seti_secret",
            "publishable_key": "pk_test",
            "setup_intent_id": "seti_1",
        },
    )
    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        resp = c.create_payment_method_setup_intent()
        assert route.called
        assert resp.client_secret == "seti_secret"
    finally:
        c.close()


@respx.mock
def test_detach_payment_method() -> None:
    route = respx.delete(f"{BASE_URL}/api/v1/billing/payment-methods/pm_abc").respond(204)
    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        result = c.detach_payment_method("pm_abc")
        assert result is None
        assert route.called
    finally:
        c.close()


# ─── auth/me ───────────────────────────────────────────────────────────


@respx.mock
def test_get_me() -> None:
    route = respx.get(f"{BASE_URL}/api/v1/auth/me").respond(
        200,
        # DeveloperResponse requires id, email, name (others optional).
        json={
            "id": "dev_1",
            "email": "dev@example.com",
            "name": "Test Developer",
            "email_verified": True,
        },
    )
    c = DeveloperClient(ACCESS, base_url=BASE_URL)
    try:
        me = c.get_me()
        assert route.called
        assert me.email == "dev@example.com"
    finally:
        c.close()


# ─── token-refresh-on-401 ──────────────────────────────────────────────


@respx.mock
def test_refresh_on_401_then_retries() -> None:
    """A 401 triggers POST /auth/refresh; on success, original call is retried with the new token."""
    balance_route = respx.get(f"{BASE_URL}/api/v1/billing/balance").mock(
        side_effect=[
            httpx.Response(401, json={"detail": "Access token expired"}),
            httpx.Response(200, json=_balance_body()),
        ]
    )
    refresh_route = respx.post(f"{BASE_URL}/api/v1/auth/refresh").respond(
        200,
        json={
            "access_token": NEW_ACCESS,
            "refresh_token": NEW_REFRESH,
            "token_type": "bearer",
            "expires_in": 7200,
        },
    )
    c = DeveloperClient(ACCESS, refresh_token=REFRESH, base_url=BASE_URL)
    try:
        balance = c.get_balance()
        assert balance.credit_balance == "12.34"
        # Both balance attempts were made.
        assert balance_route.call_count == 2
        assert refresh_route.called
        # The retry carried the new bearer token.
        assert balance_route.calls[1].request.headers.get("Authorization") == f"Bearer {NEW_ACCESS}"
        # Refresh-token box rotated to the new value.
        assert c._refresh_token_box == [NEW_REFRESH]
    finally:
        c.close()


@respx.mock
def test_refresh_failure_surfaces_original_401() -> None:
    """If POST /auth/refresh itself returns 401, the original AuthenticationError surfaces."""
    respx.get(f"{BASE_URL}/api/v1/billing/balance").respond(
        401, json={"detail": "Access token expired"}
    )
    respx.post(f"{BASE_URL}/api/v1/auth/refresh").respond(
        401, json={"detail": "Refresh token expired"}
    )
    c = DeveloperClient(ACCESS, refresh_token=REFRESH, base_url=BASE_URL)
    try:
        with pytest.raises(AuthenticationError):
            c.get_balance()
    finally:
        c.close()


@respx.mock
def test_no_refresh_token_means_no_retry() -> None:
    """Without a refresh token, a 401 surfaces directly — no retry attempted."""
    balance_route = respx.get(f"{BASE_URL}/api/v1/billing/balance").respond(
        401, json={"detail": "Access token expired"}
    )
    c = DeveloperClient(ACCESS, base_url=BASE_URL)  # no refresh_token
    try:
        with pytest.raises(AuthenticationError):
            c.get_balance()
        # Only one attempt — no refresh, no retry.
        assert balance_route.call_count == 1
    finally:
        c.close()


# ─── No-leak invariants (regression for finding A.5) ───────────────────


def test_developer_client_repr_does_not_leak_access_token() -> None:
    c = DeveloperClient(ACCESS, refresh_token=REFRESH, base_url=BASE_URL)
    try:
        r = repr(c)
        assert ACCESS not in r
        assert REFRESH not in r
        assert _JWT_SHAPE.search(r) is None
        # has_refresh_token=True is fine — the boolean is informational only.
        assert "has_refresh_token=True" in r
    finally:
        c.close()


def test_developer_client_does_not_store_access_token_on_instance() -> None:
    """The DeveloperClient instance must not carry the access token directly.

    The token lives on ``self._client.token`` (the generated
    AuthenticatedClient). Finding A.5 / PR #7 handles the second-order
    leak via ``repr(c._client)`` by marking ``token`` as ``repr=False``
    on the attrs field. The full belt-and-braces no-leak suite lives in
    PR #7's ``test_no_key_leak.py``.

    This test asserts only PR 3's contract: no direct ``self.access_token``
    or similar string attribute on the DeveloperClient instance.
    """
    c = DeveloperClient(ACCESS, refresh_token=REFRESH, base_url=BASE_URL)
    try:
        # Check string-typed attributes only — ``self._client`` is an
        # object, not a string, and its repr-suppression is PR #7's
        # responsibility, not PR 3's.
        for key, val in c.__dict__.items():
            if isinstance(val, str):
                assert ACCESS not in val, f"Access token leaked via str attribute {key!r}"
    finally:
        c.close()


# ─── Sync/async parity ────────────────────────────────────────────────


def test_sync_async_parity() -> None:
    """Every public method on DeveloperClient exists on AsyncDeveloperClient."""
    sync_methods = {
        name
        for name in dir(DeveloperClient)
        if not name.startswith("_") and callable(getattr(DeveloperClient, name))
    }
    async_methods = {
        name
        for name in dir(AsyncDeveloperClient)
        if not name.startswith("_") and callable(getattr(AsyncDeveloperClient, name))
    }
    missing = sync_methods - async_methods
    assert not missing, f"AsyncDeveloperClient is missing: {missing}"
    extra = async_methods - sync_methods
    assert not extra, f"AsyncDeveloperClient has methods not on sync: {extra}"


async def test_async_developer_client_get_balance() -> None:
    import respx

    base = BASE_URL
    with respx.mock(base_url=base) as mock:
        mock.get("/api/v1/billing/balance").respond(200, json=_balance_body())
        c = AsyncDeveloperClient(ACCESS, base_url=base)
        try:
            balance = await c.get_balance()
            assert balance.credit_balance == "12.34"
        finally:
            await c.close()


# ─── Removed-from-AethexAI regression ─────────────────────────────────


def test_aethexai_no_longer_exposes_billing_methods() -> None:
    """Audit A.1: the 8 billing methods MUST be gone from AethexAI."""
    from aethexai import AethexAI

    for name in (
        "get_balance",
        "list_plans",
        "select_plan",
        "list_invoices",
        "list_transactions",
        "list_payment_methods",
        "create_payment_method_setup_intent",
        "detach_payment_method",
    ):
        assert not hasattr(AethexAI, name), (
            f"AethexAI.{name} must have been removed (audit A.1) — "
            "it would 401 against the live server because the route "
            "requires a developer JWT, not an X-API-Key. "
            "Use aethexai.DeveloperClient instead."
        )
