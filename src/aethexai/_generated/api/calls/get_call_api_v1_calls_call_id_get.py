from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.call_response import CallResponse
from ...models.http_validation_error import HTTPValidationError
from typing import cast
from uuid import UUID


def _get_kwargs(
    call_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/calls/{call_id}".format(
            call_id=quote(str(call_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CallResponse | HTTPValidationError | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = CallResponse.from_dict(response.json())

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
) -> Response[CallResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    call_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CallResponse | HTTPValidationError]:
    """Get Call

    Args:
        call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        call_id=call_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    call_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CallResponse | HTTPValidationError | None:
    """Get Call

    Args:
        call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallResponse | HTTPValidationError
    """

    return sync_detailed(
        call_id=call_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    call_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CallResponse | HTTPValidationError]:
    """Get Call

    Args:
        call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        call_id=call_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    call_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CallResponse | HTTPValidationError | None:
    """Get Call

    Args:
        call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            call_id=call_id,
            client=client,
        )
    ).parsed
