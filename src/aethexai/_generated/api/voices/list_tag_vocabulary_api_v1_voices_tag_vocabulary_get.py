from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_tag_vocabulary_api_v1_voices_tag_vocabulary_get_response_list_tag_vocabulary_api_v1_voices_tag_vocabulary_get import (
    ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet,
)
from typing import cast


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/voices/tag-vocabulary",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet
    | None
):
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet.from_dict(
            response.json()
        )

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[
    ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet
]:
    """List Tag Vocabulary

     Return the supported set of voice tags. Requires the ``voices:read`` scope, like the rest of
    ``/voices``. Tags are grouped into categories (``tone`` / ``voice_texture`` / ``delivery_style`` /
    ``business_persona``) for presentation, but the grouping is purely cosmetic: ``GET /voices?tag=...``
    accepts any tag from any category. Tags outside this set are rejected with a 422, so this endpoint
    is the canonical place to discover the supported values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> (
    ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet
    | None
):
    """List Tag Vocabulary

     Return the supported set of voice tags. Requires the ``voices:read`` scope, like the rest of
    ``/voices``. Tags are grouped into categories (``tone`` / ``voice_texture`` / ``delivery_style`` /
    ``business_persona``) for presentation, but the grouping is purely cosmetic: ``GET /voices?tag=...``
    accepts any tag from any category. Tags outside this set are rejected with a 422, so this endpoint
    is the canonical place to discover the supported values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[
    ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet
]:
    """List Tag Vocabulary

     Return the supported set of voice tags. Requires the ``voices:read`` scope, like the rest of
    ``/voices``. Tags are grouped into categories (``tone`` / ``voice_texture`` / ``delivery_style`` /
    ``business_persona``) for presentation, but the grouping is purely cosmetic: ``GET /voices?tag=...``
    accepts any tag from any category. Tags outside this set are rejected with a 422, so this endpoint
    is the canonical place to discover the supported values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> (
    ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet
    | None
):
    """List Tag Vocabulary

     Return the supported set of voice tags. Requires the ``voices:read`` scope, like the rest of
    ``/voices``. Tags are grouped into categories (``tone`` / ``voice_texture`` / ``delivery_style`` /
    ``business_persona``) for presentation, but the grouping is purely cosmetic: ``GET /voices?tag=...``
    accepts any tag from any category. Tags outside this set are rejected with a 422, so this endpoint
    is the canonical place to discover the supported values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListTagVocabularyApiV1VoicesTagVocabularyGetResponseListTagVocabularyApiV1VoicesTagVocabularyGet
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
