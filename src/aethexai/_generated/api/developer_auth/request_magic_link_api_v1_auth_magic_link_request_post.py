from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.magic_link_request import MagicLinkRequest
from ...models.magic_link_request_response import MagicLinkRequestResponse
from typing import cast


def _get_kwargs(
    *,
    body: MagicLinkRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/auth/magic-link/request",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | MagicLinkRequestResponse | None:
    if response.status_code == 200:
        response_200 = MagicLinkRequestResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | MagicLinkRequestResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MagicLinkRequest,
) -> Response[HTTPValidationError | MagicLinkRequestResponse]:
    """Request Magic Link

     Request a one-time sign-in link by email.

    Always returns the same body on well-formed input. If the address has no
    developer row yet, the service stores only a pending email token; the
    account is created after the token is verified. 429 remains generic so
    limiter state does not become an address-discovery surface.

    Args:
        body (MagicLinkRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MagicLinkRequestResponse]
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
    body: MagicLinkRequest,
) -> HTTPValidationError | MagicLinkRequestResponse | None:
    """Request Magic Link

     Request a one-time sign-in link by email.

    Always returns the same body on well-formed input. If the address has no
    developer row yet, the service stores only a pending email token; the
    account is created after the token is verified. 429 remains generic so
    limiter state does not become an address-discovery surface.

    Args:
        body (MagicLinkRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MagicLinkRequestResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MagicLinkRequest,
) -> Response[HTTPValidationError | MagicLinkRequestResponse]:
    """Request Magic Link

     Request a one-time sign-in link by email.

    Always returns the same body on well-formed input. If the address has no
    developer row yet, the service stores only a pending email token; the
    account is created after the token is verified. 429 remains generic so
    limiter state does not become an address-discovery surface.

    Args:
        body (MagicLinkRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MagicLinkRequestResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: MagicLinkRequest,
) -> HTTPValidationError | MagicLinkRequestResponse | None:
    """Request Magic Link

     Request a one-time sign-in link by email.

    Always returns the same body on well-formed input. If the address has no
    developer row yet, the service stores only a pending email token; the
    account is created after the token is verified. 429 remains generic so
    limiter state does not become an address-discovery surface.

    Args:
        body (MagicLinkRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MagicLinkRequestResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
