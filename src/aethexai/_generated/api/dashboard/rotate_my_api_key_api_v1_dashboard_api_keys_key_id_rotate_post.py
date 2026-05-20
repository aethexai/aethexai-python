from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_key_rotate_response import APIKeyRotateResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID


def _get_kwargs(
    key_id: UUID,
    *,
    revoke_immediately: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["revoke_immediately"] = revoke_immediately

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/dashboard/api-keys/{key_id}/rotate".format(
            key_id=quote(str(key_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIKeyRotateResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = APIKeyRotateResponse.from_dict(response.json())

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
) -> Response[APIKeyRotateResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    key_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    revoke_immediately: bool | Unset = False,
) -> Response[APIKeyRotateResponse | HTTPValidationError]:
    """Rotate My Api Key

     Rotate an API key.

    Args:
        key_id (UUID):
        revoke_immediately (bool | Unset): When false (default), the old key keeps working for a
            24-hour grace period so callers can roll out the new secret without downtime; the grace
            expiry is returned as ``old_key_expires_at``. Set to true to hard-revoke the old key in
            the same call (suspected compromise); ``old_key_expires_at`` will be null in that case.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIKeyRotateResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        key_id=key_id,
        revoke_immediately=revoke_immediately,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    key_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    revoke_immediately: bool | Unset = False,
) -> APIKeyRotateResponse | HTTPValidationError | None:
    """Rotate My Api Key

     Rotate an API key.

    Args:
        key_id (UUID):
        revoke_immediately (bool | Unset): When false (default), the old key keeps working for a
            24-hour grace period so callers can roll out the new secret without downtime; the grace
            expiry is returned as ``old_key_expires_at``. Set to true to hard-revoke the old key in
            the same call (suspected compromise); ``old_key_expires_at`` will be null in that case.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIKeyRotateResponse | HTTPValidationError
    """

    return sync_detailed(
        key_id=key_id,
        client=client,
        revoke_immediately=revoke_immediately,
    ).parsed


async def asyncio_detailed(
    key_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    revoke_immediately: bool | Unset = False,
) -> Response[APIKeyRotateResponse | HTTPValidationError]:
    """Rotate My Api Key

     Rotate an API key.

    Args:
        key_id (UUID):
        revoke_immediately (bool | Unset): When false (default), the old key keeps working for a
            24-hour grace period so callers can roll out the new secret without downtime; the grace
            expiry is returned as ``old_key_expires_at``. Set to true to hard-revoke the old key in
            the same call (suspected compromise); ``old_key_expires_at`` will be null in that case.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIKeyRotateResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        key_id=key_id,
        revoke_immediately=revoke_immediately,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    key_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    revoke_immediately: bool | Unset = False,
) -> APIKeyRotateResponse | HTTPValidationError | None:
    """Rotate My Api Key

     Rotate an API key.

    Args:
        key_id (UUID):
        revoke_immediately (bool | Unset): When false (default), the old key keeps working for a
            24-hour grace period so callers can roll out the new secret without downtime; the grace
            expiry is returned as ``old_key_expires_at``. Set to true to hard-revoke the old key in
            the same call (suspected compromise); ``old_key_expires_at`` will be null in that case.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIKeyRotateResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            key_id=key_id,
            client=client,
            revoke_immediately=revoke_immediately,
        )
    ).parsed
