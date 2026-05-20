from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.developer_sessions_response import DeveloperSessionsResponse
from typing import cast


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/auth/sessions",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeveloperSessionsResponse | None:
    if response.status_code == 200:
        response_200 = DeveloperSessionsResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DeveloperSessionsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[DeveloperSessionsResponse]:
    r"""List Sessions

     List active server-side sessions for the authenticated developer.

    Surfaces the per-row state the portal uses to render a \"where you
    are signed in\" inventory. ``is_current=true`` flags the row backing
    the caller's own JWT so the UI can label it and gray out the kill
    button for it (logout is the right action for the current session).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeveloperSessionsResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> DeveloperSessionsResponse | None:
    r"""List Sessions

     List active server-side sessions for the authenticated developer.

    Surfaces the per-row state the portal uses to render a \"where you
    are signed in\" inventory. ``is_current=true`` flags the row backing
    the caller's own JWT so the UI can label it and gray out the kill
    button for it (logout is the right action for the current session).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeveloperSessionsResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[DeveloperSessionsResponse]:
    r"""List Sessions

     List active server-side sessions for the authenticated developer.

    Surfaces the per-row state the portal uses to render a \"where you
    are signed in\" inventory. ``is_current=true`` flags the row backing
    the caller's own JWT so the UI can label it and gray out the kill
    button for it (logout is the right action for the current session).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeveloperSessionsResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> DeveloperSessionsResponse | None:
    r"""List Sessions

     List active server-side sessions for the authenticated developer.

    Surfaces the per-row state the portal uses to render a \"where you
    are signed in\" inventory. ``is_current=true`` flags the row backing
    the caller's own JWT so the UI can label it and gray out the kill
    button for it (logout is the right action for the current session).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeveloperSessionsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
