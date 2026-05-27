"""Synchronous JWT-authenticated client for dashboard / billing endpoints.

The flat-method ``AethexAI`` / ``AsyncAethexAI`` clients carry an
``X-API-Key`` header and reach the ``/api/v1/{agents,calls,…}`` routes
that authenticate via ``require_api_key``. The ``/api/v1/billing/*`` and
``/api/v1/auth/me`` routes, however, require a developer-JWT bearer
token (``Authorization: Bearer <jwt>``) — issued by the magic-link
sign-in flow, the Google sign-in flow, or token refresh — and 401 on
any API-key call (audit finding A.1 in
``docs/audits/pre-launch-2026-05-17.md``).

``DeveloperClient`` is the JWT counterpart::

    from aethexai import DeveloperClient

    client = DeveloperClient(
        access_token="eyJhbGciOi...",
        refresh_token="eyJhbGciOi...",   # optional; enables auto-refresh on 401
        base_url="https://api.aethexai.com",
    )
    balance = client.get_balance()

Token-refresh contract: when an authenticated request gets a 401, the
client transparently calls ``POST /api/v1/auth/refresh`` with the
stored refresh token, swaps the access token, and retries the original
request once. If the refresh fails (or no refresh token was provided),
the original ``AuthenticationError`` surfaces.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from aethexai._body import build_body
from aethexai._exceptions import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    _map_status_to_exception,
)
from aethexai._generated.client import AuthenticatedClient
from aethexai._generated.types import UNSET, Unset

_DEFAULT_BASE_URL = "https://api.aethexai.com"


class DeveloperClient:
    """Synchronous developer-JWT client.

    Args:
        access_token: Developer JWT access token (from magic-link / Google sign-in).
            Falls back to the ``AETHEX_DEVELOPER_ACCESS_TOKEN`` env var.
        refresh_token: Optional refresh token. If provided, the client
            auto-refreshes on 401 by calling ``POST /api/v1/auth/refresh``.
            Falls back to the ``AETHEX_DEVELOPER_REFRESH_TOKEN`` env var.
        base_url: API base URL. Defaults to https://api.aethexai.com.
        timeout: Per-request timeout in seconds.
        max_retries: Number of connection-level retries (httpx transport).
        httpx_client: Optional pre-built httpx.Client to use as the transport.
    """

    def __init__(
        self,
        access_token: str | None = None,
        *,
        refresh_token: str | None = None,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 2,
        httpx_client: httpx.Client | None = None,
    ) -> None:
        resolved_access = access_token or os.environ.get("AETHEX_DEVELOPER_ACCESS_TOKEN", "")
        if not resolved_access:
            raise AuthenticationError(
                "access_token is required. Pass access_token= or set the "
                "AETHEX_DEVELOPER_ACCESS_TOKEN env var. Obtain one by completing "
                "the magic-link or Google sign-in flow at "
                "developers.aethexai.com.",
                status_code=401,
            )
        # NOTE: access/refresh tokens are intentionally NOT stored as instance
        # attributes — see ``AethexAI.__init__`` for the rationale (audit A.5).
        # The access token lives in ``self._client.token`` (with repr=False
        # applied via the post-codegen patch in ``scripts/sync_from_prod.py``);
        # the refresh token lives in the closure of ``_refresh_access_token``.
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

        resolved_refresh = refresh_token or os.environ.get("AETHEX_DEVELOPER_REFRESH_TOKEN", "")
        # Boxed so the refresh callback can rotate it atomically without
        # mutating instance state visible to introspection.
        self._refresh_token_box: list[str] = [resolved_refresh] if resolved_refresh else []

        httpx_args: dict[str, Any] = {
            "transport": httpx.HTTPTransport(retries=max_retries),
        }
        self._client = AuthenticatedClient(
            base_url=self._base_url,
            token=resolved_access,
            # Defaults: auth_header_name="Authorization", prefix="Bearer".
            timeout=httpx.Timeout(timeout),
            httpx_args=httpx_args,
        )
        if httpx_client is not None:
            self._client.set_httpx_client(httpx_client)

    # ── Lifecycle ──────────────────────────────────────────────────────

    def __repr__(self) -> str:
        # See ``AethexAI.__repr__`` — never include any field that could
        # carry the JWT access or refresh token.
        return (
            f"{type(self).__name__}(base_url={self._base_url!r}, "
            f"timeout={self._timeout!r}, "
            f"has_refresh_token={bool(self._refresh_token_box)})"
        )

    def close(self) -> None:
        """Close the underlying HTTP client."""
        inner = self._client.get_httpx_client()
        inner.close()

    def __enter__(self) -> DeveloperClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    # ── Refresh ────────────────────────────────────────────────────────

    def _refresh_access_token(self) -> bool:
        """Try to refresh the access token via the stored refresh token.

        Returns True on success (and rotates the new tokens into place),
        False if no refresh token is available or the refresh failed. Any
        exception during the refresh (network error, malformed response)
        is swallowed and surfaces as False — the caller falls back to the
        original 401.
        """
        if not self._refresh_token_box:
            return False
        refresh_token = self._refresh_token_box[0]
        try:
            from aethexai._generated.api.developer_auth import (
                refresh_api_v1_auth_refresh_post as _op,
            )
            from aethexai._generated.models.refresh_request import RefreshRequest

            response = _op.sync_detailed(
                client=self._client, body=RefreshRequest(refresh_token=refresh_token)
            )
        except Exception:
            return False
        if not 200 <= int(response.status_code) < 300:
            return False
        tokens = response.parsed
        access_token = getattr(tokens, "access_token", "") if tokens is not None else ""
        if not access_token:
            return False
        # Rotate: install the new access token onto the generated client
        # and (when present) the new refresh token in the box.
        self._client.token = access_token
        # The httpx client caches the Authorization header on first use;
        # flush it so the next request picks up the new token.
        if self._client._client is not None:
            self._client._client.headers["Authorization"] = f"Bearer {access_token}"
        new_refresh = getattr(tokens, "refresh_token", "") if tokens is not None else ""
        if new_refresh:
            self._refresh_token_box[0] = new_refresh
        return True

    # ── Internal request runner ────────────────────────────────────────

    def _call(self, op_func: Any, *args: Any, **kwargs: Any) -> Any:
        """Run a generated ``_detailed`` op, raise on non-2xx, return parsed.

        On 401, attempts a single token refresh (if a refresh token is
        available) and retries the original call. Any other status (or a
        second 401 after refresh) raises through ``_map_status_to_exception``.
        """
        try:
            response = op_func(*args, client=self._client, **kwargs)
        except httpx.TimeoutException as exc:
            raise APITimeoutError() from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(cause=exc) from exc
        status = int(response.status_code)
        if 200 <= status < 300:
            return response.parsed
        if status == 401 and self._refresh_access_token():
            try:
                response = op_func(*args, client=self._client, **kwargs)
            except httpx.TimeoutException as exc:
                raise APITimeoutError() from exc
            except httpx.HTTPError as exc:
                raise APIConnectionError(cause=exc) from exc
            status = int(response.status_code)
            if 200 <= status < 300:
                return response.parsed
        raise _map_status_to_exception(status, response.content, response.headers)

    # ── auth/me ────────────────────────────────────────────────────────

    def get_me(self) -> Any:
        """Get the current developer's profile. See https://developers.aethexai.com/docs/authentication."""
        from aethexai._generated.api.developer_auth import get_me_api_v1_auth_me_get as _op

        return self._call(_op.sync_detailed)

    def update_me(self, **fields: Any) -> Any:
        """Update the current developer's profile."""
        from aethexai._generated.api.developer_auth import update_me_api_v1_auth_me_patch as _op
        from aethexai._generated.models.developer_update import DeveloperUpdate

        return self._call(_op.sync_detailed, body=build_body(DeveloperUpdate, fields))

    def delete_me(self) -> None:
        """Delete the current developer account."""
        from aethexai._generated.api.developer_auth import (
            delete_me_api_v1_auth_me_delete as _op,
        )

        self._call(_op.sync_detailed)
        return None

    def logout(self) -> None:
        """Invalidate the current session server-side."""
        from aethexai._generated.api.developer_auth import (
            logout_api_v1_auth_logout_post as _op,
        )

        self._call(_op.sync_detailed)
        return None

    # ── billing ────────────────────────────────────────────────────────

    def get_balance(self) -> Any:
        """Get account credit balance."""
        from aethexai._generated.api.billing import get_balance_api_v1_billing_balance_get as _op

        return self._call(_op.sync_detailed)

    def list_plans(self) -> Any:
        """List available billing plans."""
        from aethexai._generated.api.billing import list_plans_api_v1_billing_plans_get as _op

        return self._call(_op.sync_detailed)

    def select_plan(self, slug: str, *, body: Any | Unset = UNSET) -> Any:
        """Select a billing plan by slug."""
        from aethexai._generated.api.billing import (
            select_plan_api_v1_billing_plans_slug_select_post as _op,
        )

        return self._call(_op.sync_detailed, slug, body=body)

    def list_invoices(
        self, *, cursor: str | None | Unset = UNSET, page_size: int | Unset = 25
    ) -> Any:
        """List tenant invoices (paginated)."""
        from aethexai._generated.api.billing import (
            list_tenant_invoices_api_v1_billing_invoices_get as _op,
        )

        return self._call(_op.sync_detailed, cursor=cursor, page_size=page_size)

    def list_transactions(
        self, *, cursor: str | None | Unset = UNSET, page_size: int | Unset = 25
    ) -> Any:
        """List billing transactions (paginated)."""
        from aethexai._generated.api.billing import (
            list_transactions_api_v1_billing_transactions_get as _op,
        )

        return self._call(_op.sync_detailed, cursor=cursor, page_size=page_size)

    def list_payment_methods(self) -> Any:
        """List saved payment methods (cards)."""
        from aethexai._generated.api.billing import (
            list_tenant_payment_methods_api_v1_billing_payment_methods_get as _op,
        )

        return self._call(_op.sync_detailed)

    def create_payment_method_setup_intent(self) -> Any:
        """Create a Stripe SetupIntent for attaching a new payment method."""
        from aethexai._generated.api.billing import (
            create_payment_method_setup_intent_api_v1_billing_payment_method_setup_intent_post as _op,
        )

        return self._call(_op.sync_detailed)

    def detach_payment_method(self, payment_method_id: str) -> None:
        """Detach a saved payment method by ID."""
        from aethexai._generated.api.billing import (
            detach_tenant_payment_method_api_v1_billing_payment_methods_payment_method_id_delete as _op,
        )

        self._call(_op.sync_detailed, payment_method_id)
        return None
