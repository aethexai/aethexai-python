from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.list_calls_api_v1_calls_get_direction_type_0 import (
    ListCallsApiV1CallsGetDirectionType0,
)
from ...models.list_calls_api_v1_calls_get_status_type_0 import ListCallsApiV1CallsGetStatusType0
from ...models.call_response import CallResponse
from ...models.paginated_response import PaginatedResponse
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    status: ListCallsApiV1CallsGetStatusType0 | None | Unset = UNSET,
    direction: ListCallsApiV1CallsGetDirectionType0 | None | Unset = UNSET,
    offset: int | Unset = 0,
    limit: int | Unset = 50,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, ListCallsApiV1CallsGetStatusType0):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    json_direction: None | str | Unset
    if isinstance(direction, Unset):
        json_direction = UNSET
    elif isinstance(direction, ListCallsApiV1CallsGetDirectionType0):
        json_direction = direction.value
    else:
        json_direction = direction
    params["direction"] = json_direction

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/calls",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PaginatedResponse | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = PaginatedResponse.from_dict(response.json())
        if response_200.data is not UNSET and response_200.data is not None:
            response_200.data = [
                CallResponse.from_dict(item) if isinstance(item, dict) else item
                for item in response_200.data
            ]
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
) -> Response[HTTPValidationError | PaginatedResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    status: ListCallsApiV1CallsGetStatusType0 | None | Unset = UNSET,
    direction: ListCallsApiV1CallsGetDirectionType0 | None | Unset = UNSET,
    offset: int | Unset = 0,
    limit: int | Unset = 50,
) -> Response[HTTPValidationError | PaginatedResponse]:
    """List Calls

    Args:
        status (ListCallsApiV1CallsGetStatusType0 | None | Unset):
        direction (ListCallsApiV1CallsGetDirectionType0 | None | Unset):
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponse]
    """

    kwargs = _get_kwargs(
        status=status,
        direction=direction,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    status: ListCallsApiV1CallsGetStatusType0 | None | Unset = UNSET,
    direction: ListCallsApiV1CallsGetDirectionType0 | None | Unset = UNSET,
    offset: int | Unset = 0,
    limit: int | Unset = 50,
) -> HTTPValidationError | PaginatedResponse | None:
    """List Calls

    Args:
        status (ListCallsApiV1CallsGetStatusType0 | None | Unset):
        direction (ListCallsApiV1CallsGetDirectionType0 | None | Unset):
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponse
    """

    return sync_detailed(
        client=client,
        status=status,
        direction=direction,
        offset=offset,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    status: ListCallsApiV1CallsGetStatusType0 | None | Unset = UNSET,
    direction: ListCallsApiV1CallsGetDirectionType0 | None | Unset = UNSET,
    offset: int | Unset = 0,
    limit: int | Unset = 50,
) -> Response[HTTPValidationError | PaginatedResponse]:
    """List Calls

    Args:
        status (ListCallsApiV1CallsGetStatusType0 | None | Unset):
        direction (ListCallsApiV1CallsGetDirectionType0 | None | Unset):
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponse]
    """

    kwargs = _get_kwargs(
        status=status,
        direction=direction,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    status: ListCallsApiV1CallsGetStatusType0 | None | Unset = UNSET,
    direction: ListCallsApiV1CallsGetDirectionType0 | None | Unset = UNSET,
    offset: int | Unset = 0,
    limit: int | Unset = 50,
) -> HTTPValidationError | PaginatedResponse | None:
    """List Calls

    Args:
        status (ListCallsApiV1CallsGetStatusType0 | None | Unset):
        direction (ListCallsApiV1CallsGetDirectionType0 | None | Unset):
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            status=status,
            direction=direction,
            offset=offset,
            limit=limit,
        )
    ).parsed
