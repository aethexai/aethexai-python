from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.recording_response import RecordingResponse
from typing import cast
from uuid import UUID


def _get_kwargs(
    recording_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/recordings/{recording_id}".format(
            recording_id=quote(str(recording_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RecordingResponse | None:
    if response.status_code == 200:
        response_200 = RecordingResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | RecordingResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    recording_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | RecordingResponse]:
    """Get Recording

    Args:
        recording_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecordingResponse]
    """

    kwargs = _get_kwargs(
        recording_id=recording_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    recording_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | RecordingResponse | None:
    """Get Recording

    Args:
        recording_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecordingResponse
    """

    return sync_detailed(
        recording_id=recording_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    recording_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | RecordingResponse]:
    """Get Recording

    Args:
        recording_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecordingResponse]
    """

    kwargs = _get_kwargs(
        recording_id=recording_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    recording_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | RecordingResponse | None:
    """Get Recording

    Args:
        recording_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecordingResponse
    """

    return (
        await asyncio_detailed(
            recording_id=recording_id,
            client=client,
        )
    ).parsed
