from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.tts_batch_response import TTSBatchResponse
from typing import cast
from uuid import UUID


def _get_kwargs(
    batch_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/tts/batch/{batch_id}".format(
            batch_id=quote(str(batch_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TTSBatchResponse | None:
    if response.status_code == 200:
        response_200 = TTSBatchResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | TTSBatchResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    batch_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | TTSBatchResponse]:
    """Get Batch

     Poll batch synthesis status. Returns presigned audio URLs for completed items.

    Args:
        batch_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TTSBatchResponse]
    """

    kwargs = _get_kwargs(
        batch_id=batch_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    batch_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | TTSBatchResponse | None:
    """Get Batch

     Poll batch synthesis status. Returns presigned audio URLs for completed items.

    Args:
        batch_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TTSBatchResponse
    """

    return sync_detailed(
        batch_id=batch_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    batch_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | TTSBatchResponse]:
    """Get Batch

     Poll batch synthesis status. Returns presigned audio URLs for completed items.

    Args:
        batch_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TTSBatchResponse]
    """

    kwargs = _get_kwargs(
        batch_id=batch_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    batch_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | TTSBatchResponse | None:
    """Get Batch

     Poll batch synthesis status. Returns presigned audio URLs for completed items.

    Args:
        batch_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TTSBatchResponse
    """

    return (
        await asyncio_detailed(
            batch_id=batch_id,
            client=client,
        )
    ).parsed
