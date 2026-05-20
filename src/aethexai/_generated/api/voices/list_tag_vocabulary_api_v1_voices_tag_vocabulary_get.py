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
    if response.status_code == 200:
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

     Return the closed-vocabulary tag set the curator UI renders.

    Gated behind ``voices:read`` so the route matches the rest of
    ``/voices/*``; tag categories are static configuration but the
    endpoint sits on the public API surface and every other voices
    listing already requires the same scope.

    The four-bucket grouping (``tone`` / ``voice_texture`` /
    ``delivery_style`` / ``business_persona``) is purely a UI affordance;
    the storage column is a flat list and ``GET /voices?tag=...``
    accepts any token from any bucket.

    The schema-layer validator (``VoiceMetadataUpdate.tags``) rejects
    tokens outside this set with a 422 that points back at this
    endpoint, so dashboards / SDK consumers have one canonical place to
    discover the supported tokens.

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

     Return the closed-vocabulary tag set the curator UI renders.

    Gated behind ``voices:read`` so the route matches the rest of
    ``/voices/*``; tag categories are static configuration but the
    endpoint sits on the public API surface and every other voices
    listing already requires the same scope.

    The four-bucket grouping (``tone`` / ``voice_texture`` /
    ``delivery_style`` / ``business_persona``) is purely a UI affordance;
    the storage column is a flat list and ``GET /voices?tag=...``
    accepts any token from any bucket.

    The schema-layer validator (``VoiceMetadataUpdate.tags``) rejects
    tokens outside this set with a 422 that points back at this
    endpoint, so dashboards / SDK consumers have one canonical place to
    discover the supported tokens.

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

     Return the closed-vocabulary tag set the curator UI renders.

    Gated behind ``voices:read`` so the route matches the rest of
    ``/voices/*``; tag categories are static configuration but the
    endpoint sits on the public API surface and every other voices
    listing already requires the same scope.

    The four-bucket grouping (``tone`` / ``voice_texture`` /
    ``delivery_style`` / ``business_persona``) is purely a UI affordance;
    the storage column is a flat list and ``GET /voices?tag=...``
    accepts any token from any bucket.

    The schema-layer validator (``VoiceMetadataUpdate.tags``) rejects
    tokens outside this set with a 422 that points back at this
    endpoint, so dashboards / SDK consumers have one canonical place to
    discover the supported tokens.

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

     Return the closed-vocabulary tag set the curator UI renders.

    Gated behind ``voices:read`` so the route matches the rest of
    ``/voices/*``; tag categories are static configuration but the
    endpoint sits on the public API surface and every other voices
    listing already requires the same scope.

    The four-bucket grouping (``tone`` / ``voice_texture`` /
    ``delivery_style`` / ``business_persona``) is purely a UI affordance;
    the storage column is a flat list and ``GET /voices?tag=...``
    accepts any token from any bucket.

    The schema-layer validator (``VoiceMetadataUpdate.tags``) rejects
    tokens outside this set with a 422 that points back at this
    endpoint, so dashboards / SDK consumers have one canonical place to
    discover the supported tokens.

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
