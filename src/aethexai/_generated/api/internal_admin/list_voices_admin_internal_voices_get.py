from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.voice_catalog_entry import VoiceCatalogEntry
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    voice_type: None | str | Unset = UNSET,
    language: None | str | Unset = UNSET,
    is_cloned: bool | None | Unset = UNSET,
    status: str | Unset = "active",
    limit: int | Unset = 500,
    offset: int | Unset = 0,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_voice_type: None | str | Unset
    if isinstance(voice_type, Unset):
        json_voice_type = UNSET
    else:
        json_voice_type = voice_type
    params["voice_type"] = json_voice_type

    json_language: None | str | Unset
    if isinstance(language, Unset):
        json_language = UNSET
    else:
        json_language = language
    params["language"] = json_language

    json_is_cloned: bool | None | Unset
    if isinstance(is_cloned, Unset):
        json_is_cloned = UNSET
    else:
        json_is_cloned = is_cloned
    params["is_cloned"] = json_is_cloned

    params["status"] = status

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/internal/voices",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[VoiceCatalogEntry] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = VoiceCatalogEntry.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[VoiceCatalogEntry]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    voice_type: None | str | Unset = UNSET,
    language: None | str | Unset = UNSET,
    is_cloned: bool | None | Unset = UNSET,
    status: str | Unset = "active",
    limit: int | Unset = 500,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | list[VoiceCatalogEntry]]:
    """List Voices Admin

     Admin-only listing of voices with full ``VoiceCatalogEntry`` shape.

    Mirrors ``GET /api/v1/voices`` live-visibility semantics (active
    voice AND active/null backing model) so the deploy/CI smoke
    discriminator selects from the same catalog customers see. Without
    the backing-model predicate the admin selector returns active
    voices backed by retired ``TtsModel`` rows that are absent from the
    public catalog; the smoke gate then picks one of those rows, fails
    to bind via ``/voices/{id}``, and silently falls back to a base
    voice, going green even when every live pool voice is gone from
    the customer surface.

    The public ``GET /voices`` deliberately omits ``voice_type`` and
    ``model_size`` (PR #978) so customers can't switch on implementation
    detail. CI smoke (``tests/test_api_smoke.sh``) and the integration-
    test fixture (``tests/api/test_voices.py``) still need to discover
    an active multispeaker pool voice so the deploy gate exercises pool
    routing end-to-end; this endpoint is the supported way to find one
    by ``voice_type``. The response carries the full curator shape
    (including ``internal_notes``) and must not be linked to from any
    customer surface.

    Filters short-circuit to a Pydantic 422 on unknown enum values
    (rather than the silent-empty behaviour of the public listing) so
    a typo in a CI script fails loudly rather than skipping the smoke
    check.

    Args:
        voice_type (None | str | Unset): Filter by materialisation type (``icl`` /
            ``singlespeaker`` / ``multispeaker``). Used by CI smoke + integration fixtures to discover
            a pool voice for the runtime round-trip after ``voice_type`` was removed from the public
            ``GET /voices`` response in PR #978. Unknown values 422.
        language (None | str | Unset): Filter by base language (``english`` / ``french`` /
            ``arabic``). Unknown values 422.
        is_cloned (bool | None | Unset): Filter by cloned-vs-global. Defaults to no filter so
            global and tenant-cloned voices are both visible to the admin.
        status (str | Unset): Filter by soft-retire status (``active`` / ``retired`` / ``all``).
            Defaults to ``active`` so smoke and integration discovery never picks a retired voice
            (which would 404 on the public detail endpoint). Default: 'active'.
        limit (int | Unset):  Default: 500.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[VoiceCatalogEntry]]
    """

    kwargs = _get_kwargs(
        voice_type=voice_type,
        language=language,
        is_cloned=is_cloned,
        status=status,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    voice_type: None | str | Unset = UNSET,
    language: None | str | Unset = UNSET,
    is_cloned: bool | None | Unset = UNSET,
    status: str | Unset = "active",
    limit: int | Unset = 500,
    offset: int | Unset = 0,
) -> HTTPValidationError | list[VoiceCatalogEntry] | None:
    """List Voices Admin

     Admin-only listing of voices with full ``VoiceCatalogEntry`` shape.

    Mirrors ``GET /api/v1/voices`` live-visibility semantics (active
    voice AND active/null backing model) so the deploy/CI smoke
    discriminator selects from the same catalog customers see. Without
    the backing-model predicate the admin selector returns active
    voices backed by retired ``TtsModel`` rows that are absent from the
    public catalog; the smoke gate then picks one of those rows, fails
    to bind via ``/voices/{id}``, and silently falls back to a base
    voice, going green even when every live pool voice is gone from
    the customer surface.

    The public ``GET /voices`` deliberately omits ``voice_type`` and
    ``model_size`` (PR #978) so customers can't switch on implementation
    detail. CI smoke (``tests/test_api_smoke.sh``) and the integration-
    test fixture (``tests/api/test_voices.py``) still need to discover
    an active multispeaker pool voice so the deploy gate exercises pool
    routing end-to-end; this endpoint is the supported way to find one
    by ``voice_type``. The response carries the full curator shape
    (including ``internal_notes``) and must not be linked to from any
    customer surface.

    Filters short-circuit to a Pydantic 422 on unknown enum values
    (rather than the silent-empty behaviour of the public listing) so
    a typo in a CI script fails loudly rather than skipping the smoke
    check.

    Args:
        voice_type (None | str | Unset): Filter by materialisation type (``icl`` /
            ``singlespeaker`` / ``multispeaker``). Used by CI smoke + integration fixtures to discover
            a pool voice for the runtime round-trip after ``voice_type`` was removed from the public
            ``GET /voices`` response in PR #978. Unknown values 422.
        language (None | str | Unset): Filter by base language (``english`` / ``french`` /
            ``arabic``). Unknown values 422.
        is_cloned (bool | None | Unset): Filter by cloned-vs-global. Defaults to no filter so
            global and tenant-cloned voices are both visible to the admin.
        status (str | Unset): Filter by soft-retire status (``active`` / ``retired`` / ``all``).
            Defaults to ``active`` so smoke and integration discovery never picks a retired voice
            (which would 404 on the public detail endpoint). Default: 'active'.
        limit (int | Unset):  Default: 500.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[VoiceCatalogEntry]
    """

    return sync_detailed(
        client=client,
        voice_type=voice_type,
        language=language,
        is_cloned=is_cloned,
        status=status,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    voice_type: None | str | Unset = UNSET,
    language: None | str | Unset = UNSET,
    is_cloned: bool | None | Unset = UNSET,
    status: str | Unset = "active",
    limit: int | Unset = 500,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | list[VoiceCatalogEntry]]:
    """List Voices Admin

     Admin-only listing of voices with full ``VoiceCatalogEntry`` shape.

    Mirrors ``GET /api/v1/voices`` live-visibility semantics (active
    voice AND active/null backing model) so the deploy/CI smoke
    discriminator selects from the same catalog customers see. Without
    the backing-model predicate the admin selector returns active
    voices backed by retired ``TtsModel`` rows that are absent from the
    public catalog; the smoke gate then picks one of those rows, fails
    to bind via ``/voices/{id}``, and silently falls back to a base
    voice, going green even when every live pool voice is gone from
    the customer surface.

    The public ``GET /voices`` deliberately omits ``voice_type`` and
    ``model_size`` (PR #978) so customers can't switch on implementation
    detail. CI smoke (``tests/test_api_smoke.sh``) and the integration-
    test fixture (``tests/api/test_voices.py``) still need to discover
    an active multispeaker pool voice so the deploy gate exercises pool
    routing end-to-end; this endpoint is the supported way to find one
    by ``voice_type``. The response carries the full curator shape
    (including ``internal_notes``) and must not be linked to from any
    customer surface.

    Filters short-circuit to a Pydantic 422 on unknown enum values
    (rather than the silent-empty behaviour of the public listing) so
    a typo in a CI script fails loudly rather than skipping the smoke
    check.

    Args:
        voice_type (None | str | Unset): Filter by materialisation type (``icl`` /
            ``singlespeaker`` / ``multispeaker``). Used by CI smoke + integration fixtures to discover
            a pool voice for the runtime round-trip after ``voice_type`` was removed from the public
            ``GET /voices`` response in PR #978. Unknown values 422.
        language (None | str | Unset): Filter by base language (``english`` / ``french`` /
            ``arabic``). Unknown values 422.
        is_cloned (bool | None | Unset): Filter by cloned-vs-global. Defaults to no filter so
            global and tenant-cloned voices are both visible to the admin.
        status (str | Unset): Filter by soft-retire status (``active`` / ``retired`` / ``all``).
            Defaults to ``active`` so smoke and integration discovery never picks a retired voice
            (which would 404 on the public detail endpoint). Default: 'active'.
        limit (int | Unset):  Default: 500.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[VoiceCatalogEntry]]
    """

    kwargs = _get_kwargs(
        voice_type=voice_type,
        language=language,
        is_cloned=is_cloned,
        status=status,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    voice_type: None | str | Unset = UNSET,
    language: None | str | Unset = UNSET,
    is_cloned: bool | None | Unset = UNSET,
    status: str | Unset = "active",
    limit: int | Unset = 500,
    offset: int | Unset = 0,
) -> HTTPValidationError | list[VoiceCatalogEntry] | None:
    """List Voices Admin

     Admin-only listing of voices with full ``VoiceCatalogEntry`` shape.

    Mirrors ``GET /api/v1/voices`` live-visibility semantics (active
    voice AND active/null backing model) so the deploy/CI smoke
    discriminator selects from the same catalog customers see. Without
    the backing-model predicate the admin selector returns active
    voices backed by retired ``TtsModel`` rows that are absent from the
    public catalog; the smoke gate then picks one of those rows, fails
    to bind via ``/voices/{id}``, and silently falls back to a base
    voice, going green even when every live pool voice is gone from
    the customer surface.

    The public ``GET /voices`` deliberately omits ``voice_type`` and
    ``model_size`` (PR #978) so customers can't switch on implementation
    detail. CI smoke (``tests/test_api_smoke.sh``) and the integration-
    test fixture (``tests/api/test_voices.py``) still need to discover
    an active multispeaker pool voice so the deploy gate exercises pool
    routing end-to-end; this endpoint is the supported way to find one
    by ``voice_type``. The response carries the full curator shape
    (including ``internal_notes``) and must not be linked to from any
    customer surface.

    Filters short-circuit to a Pydantic 422 on unknown enum values
    (rather than the silent-empty behaviour of the public listing) so
    a typo in a CI script fails loudly rather than skipping the smoke
    check.

    Args:
        voice_type (None | str | Unset): Filter by materialisation type (``icl`` /
            ``singlespeaker`` / ``multispeaker``). Used by CI smoke + integration fixtures to discover
            a pool voice for the runtime round-trip after ``voice_type`` was removed from the public
            ``GET /voices`` response in PR #978. Unknown values 422.
        language (None | str | Unset): Filter by base language (``english`` / ``french`` /
            ``arabic``). Unknown values 422.
        is_cloned (bool | None | Unset): Filter by cloned-vs-global. Defaults to no filter so
            global and tenant-cloned voices are both visible to the admin.
        status (str | Unset): Filter by soft-retire status (``active`` / ``retired`` / ``all``).
            Defaults to ``active`` so smoke and integration discovery never picks a retired voice
            (which would 404 on the public detail endpoint). Default: 'active'.
        limit (int | Unset):  Default: 500.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[VoiceCatalogEntry]
    """

    return (
        await asyncio_detailed(
            client=client,
            voice_type=voice_type,
            language=language,
            is_cloned=is_cloned,
            status=status,
            limit=limit,
            offset=offset,
        )
    ).parsed
