from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.sip_trunk_response import SipTrunkResponse
from typing import cast
from uuid import UUID


def _get_kwargs(
    trunk_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/sip-trunks/{trunk_id}".format(
            trunk_id=quote(str(trunk_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | SipTrunkResponse | None:
    if response.status_code == 200:
        response_200 = SipTrunkResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | SipTrunkResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    trunk_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | SipTrunkResponse]:
    """Get Sip Trunk

    Args:
        trunk_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SipTrunkResponse]
    """

    kwargs = _get_kwargs(
        trunk_id=trunk_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    trunk_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | SipTrunkResponse | None:
    """Get Sip Trunk

    Args:
        trunk_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SipTrunkResponse
    """

    return sync_detailed(
        trunk_id=trunk_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    trunk_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | SipTrunkResponse]:
    """Get Sip Trunk

    Args:
        trunk_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SipTrunkResponse]
    """

    kwargs = _get_kwargs(
        trunk_id=trunk_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    trunk_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | SipTrunkResponse | None:
    """Get Sip Trunk

    Args:
        trunk_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SipTrunkResponse
    """

    return (
        await asyncio_detailed(
            trunk_id=trunk_id,
            client=client,
        )
    ).parsed
