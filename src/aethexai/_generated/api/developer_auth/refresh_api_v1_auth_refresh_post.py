from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_tokens import AuthTokens
from ...models.http_validation_error import HTTPValidationError
from ...models.refresh_request import RefreshRequest
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    body: None | RefreshRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/auth/refresh",
    }

    if isinstance(body, RefreshRequest):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AuthTokens | HTTPValidationError | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = AuthTokens.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AuthTokens | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: None | RefreshRequest | Unset = UNSET,
) -> Response[AuthTokens | HTTPValidationError]:
    """Refresh

     Rotate the developer's access/refresh pair. Accepts the refresh token from the
    ``aethex_refresh_token`` HttpOnly
    cookie (preferred) or the request body (legacy / non-browser
    callers). The cookie lane is additionally CSRF-checked (double-submit
    ``X-CSRF-Token`` matches ``aethex_csrf_token``). This route does
    not depend on ``require_developer_jwt`` — by design, since the
    refresh token can be valid when the access token has expired —
    so the CSRF guard is wired here explicitly. Without it, a
    same-site sub-domain that gained XHR foothold could ride the
    victim's refresh cookie to advance ``refresh_generation`` /
    burn budget / log them out via rotation-anomaly detection. Body-token callers (no cookie present)
    skip the check.

    Args:
        body (None | RefreshRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthTokens | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: None | RefreshRequest | Unset = UNSET,
) -> AuthTokens | HTTPValidationError | None:
    """Refresh

     Rotate the developer's access/refresh pair. Accepts the refresh token from the
    ``aethex_refresh_token`` HttpOnly
    cookie (preferred) or the request body (legacy / non-browser
    callers). The cookie lane is additionally CSRF-checked (double-submit
    ``X-CSRF-Token`` matches ``aethex_csrf_token``). This route does
    not depend on ``require_developer_jwt`` — by design, since the
    refresh token can be valid when the access token has expired —
    so the CSRF guard is wired here explicitly. Without it, a
    same-site sub-domain that gained XHR foothold could ride the
    victim's refresh cookie to advance ``refresh_generation`` /
    burn budget / log them out via rotation-anomaly detection. Body-token callers (no cookie present)
    skip the check.

    Args:
        body (None | RefreshRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthTokens | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: None | RefreshRequest | Unset = UNSET,
) -> Response[AuthTokens | HTTPValidationError]:
    """Refresh

     Rotate the developer's access/refresh pair. Accepts the refresh token from the
    ``aethex_refresh_token`` HttpOnly
    cookie (preferred) or the request body (legacy / non-browser
    callers). The cookie lane is additionally CSRF-checked (double-submit
    ``X-CSRF-Token`` matches ``aethex_csrf_token``). This route does
    not depend on ``require_developer_jwt`` — by design, since the
    refresh token can be valid when the access token has expired —
    so the CSRF guard is wired here explicitly. Without it, a
    same-site sub-domain that gained XHR foothold could ride the
    victim's refresh cookie to advance ``refresh_generation`` /
    burn budget / log them out via rotation-anomaly detection. Body-token callers (no cookie present)
    skip the check.

    Args:
        body (None | RefreshRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthTokens | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: None | RefreshRequest | Unset = UNSET,
) -> AuthTokens | HTTPValidationError | None:
    """Refresh

     Rotate the developer's access/refresh pair. Accepts the refresh token from the
    ``aethex_refresh_token`` HttpOnly
    cookie (preferred) or the request body (legacy / non-browser
    callers). The cookie lane is additionally CSRF-checked (double-submit
    ``X-CSRF-Token`` matches ``aethex_csrf_token``). This route does
    not depend on ``require_developer_jwt`` — by design, since the
    refresh token can be valid when the access token has expired —
    so the CSRF guard is wired here explicitly. Without it, a
    same-site sub-domain that gained XHR foothold could ride the
    victim's refresh cookie to advance ``refresh_generation`` /
    burn budget / log them out via rotation-anomaly detection. Body-token callers (no cookie present)
    skip the check.

    Args:
        body (None | RefreshRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthTokens | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
