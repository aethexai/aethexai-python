from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID


def _get_kwargs(
    conversation_id: UUID,
    *,
    token: None | str | Unset = UNSET,
    range_: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(range_, Unset):
        headers["Range"] = range_

    params: dict[str, Any] = {}

    json_token: None | str | Unset
    if isinstance(token, Unset):
        json_token = UNSET
    else:
        json_token = token
    params["token"] = json_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/conversations/{conversation_id}/audio.wav".format(
            conversation_id=quote(str(conversation_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    conversation_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    token: None | str | Unset = UNSET,
    range_: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Stream Audio

     Stream the conversation audio. Bucket and region are never exposed. The Content-Type is still taken
    from the underlying recording (via
    ``_FORMAT_CONTENT_TYPES``) so a future non-WAV writer would be served
    correctly without re-introducing a per-format route. Auth: either a signed ``?token=`` issued by
    ``GET /audio`` (lets browsers
    embed the URL in an ``<audio>`` tag without headers), or a normal
    ``X-API-Key`` / ``Authorization: Bearer`` API key with the
    ``conversations:read`` scope.

    Args:
        conversation_id (UUID):
        token (None | str | Unset):
        range_ (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        conversation_id=conversation_id,
        token=token,
        range_=range_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    conversation_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    token: None | str | Unset = UNSET,
    range_: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Stream Audio

     Stream the conversation audio. Bucket and region are never exposed. The Content-Type is still taken
    from the underlying recording (via
    ``_FORMAT_CONTENT_TYPES``) so a future non-WAV writer would be served
    correctly without re-introducing a per-format route. Auth: either a signed ``?token=`` issued by
    ``GET /audio`` (lets browsers
    embed the URL in an ``<audio>`` tag without headers), or a normal
    ``X-API-Key`` / ``Authorization: Bearer`` API key with the
    ``conversations:read`` scope.

    Args:
        conversation_id (UUID):
        token (None | str | Unset):
        range_ (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        conversation_id=conversation_id,
        client=client,
        token=token,
        range_=range_,
    ).parsed


async def asyncio_detailed(
    conversation_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    token: None | str | Unset = UNSET,
    range_: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Stream Audio

     Stream the conversation audio. Bucket and region are never exposed. The Content-Type is still taken
    from the underlying recording (via
    ``_FORMAT_CONTENT_TYPES``) so a future non-WAV writer would be served
    correctly without re-introducing a per-format route. Auth: either a signed ``?token=`` issued by
    ``GET /audio`` (lets browsers
    embed the URL in an ``<audio>`` tag without headers), or a normal
    ``X-API-Key`` / ``Authorization: Bearer`` API key with the
    ``conversations:read`` scope.

    Args:
        conversation_id (UUID):
        token (None | str | Unset):
        range_ (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        conversation_id=conversation_id,
        token=token,
        range_=range_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    conversation_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    token: None | str | Unset = UNSET,
    range_: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Stream Audio

     Stream the conversation audio. Bucket and region are never exposed. The Content-Type is still taken
    from the underlying recording (via
    ``_FORMAT_CONTENT_TYPES``) so a future non-WAV writer would be served
    correctly without re-introducing a per-format route. Auth: either a signed ``?token=`` issued by
    ``GET /audio`` (lets browsers
    embed the URL in an ``<audio>`` tag without headers), or a normal
    ``X-API-Key`` / ``Authorization: Bearer`` API key with the
    ``conversations:read`` scope.

    Args:
        conversation_id (UUID):
        token (None | str | Unset):
        range_ (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            conversation_id=conversation_id,
            client=client,
            token=token,
            range_=range_,
        )
    ).parsed
