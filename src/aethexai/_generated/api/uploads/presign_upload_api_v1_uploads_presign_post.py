from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.presign_upload_request import PresignUploadRequest
from ...models.presign_upload_response import PresignUploadResponse
from typing import cast


def _get_kwargs(
    *,
    body: PresignUploadRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/uploads/presign",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PresignUploadResponse | None:
    if response.status_code == 200:
        response_200 = PresignUploadResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | PresignUploadResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: PresignUploadRequest,
) -> Response[HTTPValidationError | PresignUploadResponse]:
    """Get a presigned URL to upload a file directly to storage

     Binary bodies bypass the API ALB/WAF. After the PUT succeeds, pass `upload_id` to the consuming
    endpoint (e.g. `POST /transcribe/by-upload`).

    Args:
        body (PresignUploadRequest): Ask the server for a presigned URL the client can PUT a file
            to.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PresignUploadResponse]
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
    body: PresignUploadRequest,
) -> HTTPValidationError | PresignUploadResponse | None:
    """Get a presigned URL to upload a file directly to storage

     Binary bodies bypass the API ALB/WAF. After the PUT succeeds, pass `upload_id` to the consuming
    endpoint (e.g. `POST /transcribe/by-upload`).

    Args:
        body (PresignUploadRequest): Ask the server for a presigned URL the client can PUT a file
            to.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PresignUploadResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PresignUploadRequest,
) -> Response[HTTPValidationError | PresignUploadResponse]:
    """Get a presigned URL to upload a file directly to storage

     Binary bodies bypass the API ALB/WAF. After the PUT succeeds, pass `upload_id` to the consuming
    endpoint (e.g. `POST /transcribe/by-upload`).

    Args:
        body (PresignUploadRequest): Ask the server for a presigned URL the client can PUT a file
            to.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PresignUploadResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: PresignUploadRequest,
) -> HTTPValidationError | PresignUploadResponse | None:
    """Get a presigned URL to upload a file directly to storage

     Binary bodies bypass the API ALB/WAF. After the PUT succeeds, pass `upload_id` to the consuming
    endpoint (e.g. `POST /transcribe/by-upload`).

    Args:
        body (PresignUploadRequest): Ask the server for a presigned URL the client can PUT a file
            to.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PresignUploadResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
