from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.voice_response import VoiceResponse
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    language: None | str | Unset = UNSET,
    supports_dialect_style: bool | None | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_language: None | str | Unset
    if isinstance(language, Unset):
        json_language = UNSET
    else:
        json_language = language
    params["language"] = json_language

    json_supports_dialect_style: bool | None | Unset
    if isinstance(supports_dialect_style, Unset):
        json_supports_dialect_style = UNSET
    else:
        json_supports_dialect_style = supports_dialect_style
    params["supports_dialect_style"] = json_supports_dialect_style

    json_tag: None | str | Unset
    if isinstance(tag, Unset):
        json_tag = UNSET
    else:
        json_tag = tag
    params["tag"] = json_tag

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/voices",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[VoiceResponse] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = VoiceResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[VoiceResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    language: None | str | Unset = UNSET,
    supports_dialect_style: bool | None | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | list[VoiceResponse]]:
    """List Voices

    Args:
        language (None | str | Unset):
        supports_dialect_style (bool | None | Unset):
        tag (None | str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[VoiceResponse]]
    """

    kwargs = _get_kwargs(
        language=language,
        supports_dialect_style=supports_dialect_style,
        tag=tag,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    language: None | str | Unset = UNSET,
    supports_dialect_style: bool | None | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> HTTPValidationError | list[VoiceResponse] | None:
    """List Voices

    Args:
        language (None | str | Unset):
        supports_dialect_style (bool | None | Unset):
        tag (None | str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[VoiceResponse]
    """

    return sync_detailed(
        client=client,
        language=language,
        supports_dialect_style=supports_dialect_style,
        tag=tag,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    language: None | str | Unset = UNSET,
    supports_dialect_style: bool | None | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | list[VoiceResponse]]:
    """List Voices

    Args:
        language (None | str | Unset):
        supports_dialect_style (bool | None | Unset):
        tag (None | str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[VoiceResponse]]
    """

    kwargs = _get_kwargs(
        language=language,
        supports_dialect_style=supports_dialect_style,
        tag=tag,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    language: None | str | Unset = UNSET,
    supports_dialect_style: bool | None | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> HTTPValidationError | list[VoiceResponse] | None:
    """List Voices

    Args:
        language (None | str | Unset):
        supports_dialect_style (bool | None | Unset):
        tag (None | str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[VoiceResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            language=language,
            supports_dialect_style=supports_dialect_style,
            tag=tag,
            limit=limit,
            offset=offset,
        )
    ).parsed
