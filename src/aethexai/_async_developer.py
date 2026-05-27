"""Asynchronous JWT-authenticated client for dashboard / billing endpoints.

Mirrors ``developer.DeveloperClient`` 1:1 — every method has an
identically-named ``async def`` here and dispatches the matching
generated ``asyncio_detailed`` op.

See ``developer.py`` for the design rationale (audit finding A.1).
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


class AsyncDeveloperClient:
    """Asynchronous developer-JWT client. See ``DeveloperClient`` for usage."""

    def __init__(
        self,
        access_token: str | None = None,
        *,
        refresh_token: str | None = None,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 2,
        httpx_client: httpx.AsyncClient | None = None,
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
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

        resolved_refresh = refresh_token or os.environ.get("AETHEX_DEVELOPER_REFRESH_TOKEN", "")
        self._refresh_token_box: list[str] = [resolved_refresh] if resolved_refresh else []

        httpx_args: dict[str, Any] = {
            "transport": httpx.AsyncHTTPTransport(retries=max_retries),
        }
        self._client = AuthenticatedClient(
            base_url=self._base_url,
            token=resolved_access,
            timeout=httpx.Timeout(timeout),
            httpx_args=httpx_args,
        )
        if httpx_client is not None:
            self._client.set_async_httpx_client(httpx_client)

    # ── Lifecycle ──────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(base_url={self._base_url!r}, "
            f"timeout={self._timeout!r}, "
            f"has_refresh_token={bool(self._refresh_token_box)})"
        )

    async def close(self) -> None:
        """Close the underlying async HTTP client."""
        inner = self._client.get_async_httpx_client()
        await inner.aclose()

    async def __aenter__(self) -> AsyncDeveloperClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    # ── Refresh ────────────────────────────────────────────────────────

    async def _refresh_access_token(self) -> bool:
        if not self._refresh_token_box:
            return False
        refresh_token = self._refresh_token_box[0]
        try:
            from aethexai._generated.api.developer_auth import (
                refresh_api_v1_auth_refresh_post as _op,
            )
            from aethexai._generated.models.refresh_request import RefreshRequest

            response = await _op.asyncio_detailed(
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
        self._client.token = access_token
        if self._client._async_client is not None:
            self._client._async_client.headers["Authorization"] = f"Bearer {access_token}"
        new_refresh = getattr(tokens, "refresh_token", "") if tokens is not None else ""
        if new_refresh:
            self._refresh_token_box[0] = new_refresh
        return True

    # ── Internal request runner ────────────────────────────────────────

    async def _call(self, op_func: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            response = await op_func(*args, client=self._client, **kwargs)
        except httpx.TimeoutException as exc:
            raise APITimeoutError() from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(cause=exc) from exc
        status = int(response.status_code)
        if 200 <= status < 300:
            return response.parsed
        if status == 401 and await self._refresh_access_token():
            try:
                response = await op_func(*args, client=self._client, **kwargs)
            except httpx.TimeoutException as exc:
                raise APITimeoutError() from exc
            except httpx.HTTPError as exc:
                raise APIConnectionError(cause=exc) from exc
            status = int(response.status_code)
            if 200 <= status < 300:
                return response.parsed
        raise _map_status_to_exception(status, response.content, response.headers)

    # ── auth/me ────────────────────────────────────────────────────────

    async def get_me(self) -> Any:
        """Get the current developer's profile."""
        from aethexai._generated.api.developer_auth import get_me_api_v1_auth_me_get as _op

        return await self._call(_op.asyncio_detailed)

    async def update_me(self, **fields: Any) -> Any:
        """Update the current developer's profile."""
        from aethexai._generated.api.developer_auth import (
            update_me_api_v1_auth_me_patch as _op,
        )
        from aethexai._generated.models.developer_update import DeveloperUpdate

        return await self._call(_op.asyncio_detailed, body=build_body(DeveloperUpdate, fields))

    async def delete_me(self) -> None:
        """Delete the current developer account."""
        from aethexai._generated.api.developer_auth import (
            delete_me_api_v1_auth_me_delete as _op,
        )

        await self._call(_op.asyncio_detailed)
        return None

    async def logout(self) -> None:
        """Invalidate the current session server-side."""
        from aethexai._generated.api.developer_auth import (
            logout_api_v1_auth_logout_post as _op,
        )

        await self._call(_op.asyncio_detailed)
        return None

    # ── billing ────────────────────────────────────────────────────────

    async def get_balance(self) -> Any:
        from aethexai._generated.api.billing import get_balance_api_v1_billing_balance_get as _op

        return await self._call(_op.asyncio_detailed)

    async def list_plans(self) -> Any:
        from aethexai._generated.api.billing import list_plans_api_v1_billing_plans_get as _op

        return await self._call(_op.asyncio_detailed)

    async def select_plan(self, slug: str, *, body: Any | None = None) -> Any:
        from aethexai._generated.api.billing import (
            select_plan_api_v1_billing_plans_slug_select_post as _op,
        )

        return await self._call(_op.asyncio_detailed, slug, body=body)

    async def list_invoices(
        self, *, cursor: str | None | Unset = UNSET, page_size: int | Unset = 25
    ) -> Any:
        from aethexai._generated.api.billing import (
            list_tenant_invoices_api_v1_billing_invoices_get as _op,
        )

        return await self._call(_op.asyncio_detailed, cursor=cursor, page_size=page_size)

    async def list_transactions(
        self, *, cursor: str | None | Unset = UNSET, page_size: int | Unset = 25
    ) -> Any:
        from aethexai._generated.api.billing import (
            list_transactions_api_v1_billing_transactions_get as _op,
        )

        return await self._call(_op.asyncio_detailed, cursor=cursor, page_size=page_size)

    async def list_payment_methods(self) -> Any:
        from aethexai._generated.api.billing import (
            list_tenant_payment_methods_api_v1_billing_payment_methods_get as _op,
        )

        return await self._call(_op.asyncio_detailed)

    async def create_payment_method_setup_intent(self) -> Any:
        from aethexai._generated.api.billing import (
            create_payment_method_setup_intent_api_v1_billing_payment_method_setup_intent_post as _op,
        )

        return await self._call(_op.asyncio_detailed)

    async def detach_payment_method(self, payment_method_id: str) -> None:
        from aethexai._generated.api.billing import (
            detach_tenant_payment_method_api_v1_billing_payment_methods_payment_method_id_delete as _op,
        )

        await self._call(_op.asyncio_detailed, payment_method_id)
        return None
