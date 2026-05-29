from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.google_auth_response import GoogleAuthResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.magic_link_verify_request import MagicLinkVerifyRequest
from typing import cast


def _get_kwargs(
    *,
    body: MagicLinkVerifyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/auth/magic-link/verify",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GoogleAuthResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = GoogleAuthResponse.from_dict(response.json())

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
) -> Response[GoogleAuthResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MagicLinkVerifyRequest,
) -> Response[GoogleAuthResponse | HTTPValidationError]:
    """Verify Magic Link

     Consume a magic-link token; return JWT pair + optional first API key. Response schema matches
    ``GoogleAuthResponse`` on purpose — the
    portal's ``saveAuth`` + first-sign-in API-key reveal flows key off
    this shape and we want zero client-side branching between the two
    sign-in methods. Rate-limited per-IP so a leaked-log dump of partial tokens can't be
    brute-scanned at full speed. The token space is already 256 bits so
    this is defence-in-depth, not the primary control.

    Args:
        body (MagicLinkVerifyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GoogleAuthResponse | HTTPValidationError]
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
    body: MagicLinkVerifyRequest,
) -> GoogleAuthResponse | HTTPValidationError | None:
    """Verify Magic Link

     Consume a magic-link token; return JWT pair + optional first API key. Response schema matches
    ``GoogleAuthResponse`` on purpose — the
    portal's ``saveAuth`` + first-sign-in API-key reveal flows key off
    this shape and we want zero client-side branching between the two
    sign-in methods. Rate-limited per-IP so a leaked-log dump of partial tokens can't be
    brute-scanned at full speed. The token space is already 256 bits so
    this is defence-in-depth, not the primary control.

    Args:
        body (MagicLinkVerifyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GoogleAuthResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MagicLinkVerifyRequest,
) -> Response[GoogleAuthResponse | HTTPValidationError]:
    """Verify Magic Link

     Consume a magic-link token; return JWT pair + optional first API key. Response schema matches
    ``GoogleAuthResponse`` on purpose — the
    portal's ``saveAuth`` + first-sign-in API-key reveal flows key off
    this shape and we want zero client-side branching between the two
    sign-in methods. Rate-limited per-IP so a leaked-log dump of partial tokens can't be
    brute-scanned at full speed. The token space is already 256 bits so
    this is defence-in-depth, not the primary control.

    Args:
        body (MagicLinkVerifyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GoogleAuthResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: MagicLinkVerifyRequest,
) -> GoogleAuthResponse | HTTPValidationError | None:
    """Verify Magic Link

     Consume a magic-link token; return JWT pair + optional first API key. Response schema matches
    ``GoogleAuthResponse`` on purpose — the
    portal's ``saveAuth`` + first-sign-in API-key reveal flows key off
    this shape and we want zero client-side branching between the two
    sign-in methods. Rate-limited per-IP so a leaked-log dump of partial tokens can't be
    brute-scanned at full speed. The token space is already 256 bits so
    this is defence-in-depth, not the primary control.

    Args:
        body (MagicLinkVerifyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GoogleAuthResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
