from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.tts_batch_create import TTSBatchCreate
from ...models.tts_batch_response import TTSBatchResponse
from typing import cast


def _get_kwargs(
    *,
    body: TTSBatchCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/tts/batch",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TTSBatchResponse | None:
    if response.status_code == 201:
        response_201 = TTSBatchResponse.from_dict(response.json())

        return response_201

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
    *,
    client: AuthenticatedClient,
    body: TTSBatchCreate,
) -> Response[HTTPValidationError | TTSBatchResponse]:
    """Batch Synthesize

     Batch synthesis — submit multiple texts, get a batch_id for polling. Audio files are stored in S3.
    Poll GET /tts/batch/{batch_id} for
    presigned download URLs when complete. Usage metering is deferred to the worker (run_tts_batch) so
    only
    successfully synthesized items are billed.

    Args:
        body (TTSBatchCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TTSBatchResponse]
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
    client: AuthenticatedClient,
    body: TTSBatchCreate,
) -> HTTPValidationError | TTSBatchResponse | None:
    """Batch Synthesize

     Batch synthesis — submit multiple texts, get a batch_id for polling. Audio files are stored in S3.
    Poll GET /tts/batch/{batch_id} for
    presigned download URLs when complete. Usage metering is deferred to the worker (run_tts_batch) so
    only
    successfully synthesized items are billed.

    Args:
        body (TTSBatchCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TTSBatchResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TTSBatchCreate,
) -> Response[HTTPValidationError | TTSBatchResponse]:
    """Batch Synthesize

     Batch synthesis — submit multiple texts, get a batch_id for polling. Audio files are stored in S3.
    Poll GET /tts/batch/{batch_id} for
    presigned download URLs when complete. Usage metering is deferred to the worker (run_tts_batch) so
    only
    successfully synthesized items are billed.

    Args:
        body (TTSBatchCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TTSBatchResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TTSBatchCreate,
) -> HTTPValidationError | TTSBatchResponse | None:
    """Batch Synthesize

     Batch synthesis — submit multiple texts, get a batch_id for polling. Audio files are stored in S3.
    Poll GET /tts/batch/{batch_id} for
    presigned download URLs when complete. Usage metering is deferred to the worker (run_tts_batch) so
    only
    successfully synthesized items are billed.

    Args:
        body (TTSBatchCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TTSBatchResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
