from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.logout_all_response import LogoutAllResponse
from typing import cast


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/auth/logout-all",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> LogoutAllResponse | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = LogoutAllResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[LogoutAllResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[LogoutAllResponse]:
    """Logout All

     Revoke every active session for the developer. Rate-limited per-developer so a stolen access token
    cannot be used
    to repeatedly burn the legitimate user's recovery path. The cookies
    on this response are cleared because the caller's own session is
    among those revoked.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LogoutAllResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> LogoutAllResponse | None:
    """Logout All

     Revoke every active session for the developer. Rate-limited per-developer so a stolen access token
    cannot be used
    to repeatedly burn the legitimate user's recovery path. The cookies
    on this response are cleared because the caller's own session is
    among those revoked.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LogoutAllResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[LogoutAllResponse]:
    """Logout All

     Revoke every active session for the developer. Rate-limited per-developer so a stolen access token
    cannot be used
    to repeatedly burn the legitimate user's recovery path. The cookies
    on this response are cleared because the caller's own session is
    among those revoked.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LogoutAllResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> LogoutAllResponse | None:
    """Logout All

     Revoke every active session for the developer. Rate-limited per-developer so a stolen access token
    cannot be used
    to repeatedly burn the legitimate user's recovery path. The cookies
    on this response are cleared because the caller's own session is
    among those revoked.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LogoutAllResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
