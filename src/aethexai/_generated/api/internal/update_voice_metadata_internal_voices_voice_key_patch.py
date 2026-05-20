from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.voice_catalog_entry import VoiceCatalogEntry
from ...models.voice_metadata_update import VoiceMetadataUpdate
from typing import cast


def _get_kwargs(
    voice_key: str,
    *,
    body: VoiceMetadataUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/internal/voices/{voice_key}".format(
            voice_key=quote(str(voice_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | VoiceCatalogEntry | None:
    if response.status_code == 200:
        response_200 = VoiceCatalogEntry.from_dict(response.json())

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
) -> Response[HTTPValidationError | VoiceCatalogEntry]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    voice_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: VoiceMetadataUpdate,
) -> Response[HTTPValidationError | VoiceCatalogEntry]:
    r"""Update Voice Metadata

     Update curator-editable fields on a global voice.

    Editable fields (all optional; omit a key to leave it unchanged):

    * ``display_name`` — curator-authored override for the customer-
      facing voice name. ``null`` clears the override and the public
      ``name`` reverts to the migrated value.
    * ``status`` — soft-retire flag. ``\"active\"`` shows the voice on
      ``GET /voices``; ``\"retired\"`` hides it from listings and 404s
      ``GET /voices/{voice_id}`` while leaving the row (and the
      internal voice-registry consumed by the TTS pod) untouched.
    * ``description`` — customer-facing one-liner; ``null`` clears.
      Brand-leak validated like ``display_name``.
    * ``internal_notes`` — admin-only commentary, never copied onto the
      public ``VoiceResponse``. ``null`` clears.
    * ``tags`` — closed-vocabulary list of tokens drawn from
      :data:`aethex.models.voice.VOICE_TAG_VOCABULARY`. ``[]`` clears;
      sending ``null`` is rejected because the column is NOT NULL.
    * ``gender`` — curator-authored correction for the speaker's
      perceived gender (``male`` / ``female`` / ``neutral``). The seed
      value is best-effort and known to be wrong on some pool voices.
      Sending ``null`` is rejected because the column is NOT NULL;
      an out-of-set value 422s with the field path.

    All flow through ``body.model_dump(exclude_unset=True)`` so a single
    PATCH can update any combination of fields.

    Scoped to ``tenant_id IS NULL`` (tenant-cloned voices are not
    editable through this endpoint). The ``Voice.public_name`` property
    is the single source of truth for the ``display_name or name``
    fallback chain so this endpoint and ``_voice_to_response`` cannot
    drift.

    Auth comes from the router-level ``X-Internal-Auth`` dependency.
    Unknown keys are silently dropped (``extra='ignore'``) so a rolling
    deploy that adds a new metadata field on the API side, or one that
    adds it on the dashboard side first, does not 422 the curator out
    of a save during the window where the two halves disagree on shape.
    The body schema still enforces oversize strings, any ``display_name``
    / ``description`` value that looks like an internal voice_key or
    carries a known brand-leak token, any ``status`` outside
    ``('active', 'retired')``, and any ``tags`` entry outside the
    closed vocabulary.

    Args:
        voice_key (str):
        body (VoiceMetadataUpdate): Body for ``PATCH /internal/voices/{voice_key}``.

            Editable fields:

            * ``display_name``: curator-authored override for the customer-facing
              voice name. The migrated ``name`` value is the durable fallback;
              setting this to ``null`` clears the override and the response reverts
              to the migrated name.
            * ``status``: soft-retire flag. ``"active"`` shows the voice on
              ``GET /voices``; ``"retired"`` hides it from listings and 404s
              ``GET /voices/{voice_id}`` while leaving the row (and the internal
              voice-registry consumed by the TTS pod) untouched.
            * ``description``: customer-facing one-liner. Brand-leak validated
              like ``display_name``.
            * ``internal_notes``: admin-only commentary, never copied onto the
              public ``VoiceResponse``. No brand-leak scrub because the field is
              meant to hold context that legitimately names internal voices.
            * ``tags``: closed-vocabulary list of tokens drawn from
              :data:`VOICE_TAG_VOCABULARY`. Send ``[]`` to clear; sending
              ``null`` is rejected because the underlying column is NOT NULL.
            * ``gender``: curator-authored correction for the speaker's perceived
              gender. The seed gender is best-effort and is known to be wrong on
              some pool voices, so the dashboard exposes a male/female/neutral
              selector that PATCHes the canonical value here. Sending ``null``
              is rejected because the underlying column is NOT NULL; omit the
              key to leave the existing value unchanged.

            Every field is optional. Omitting a key leaves the column untouched
            via ``model_dump(exclude_unset=True)``; sending ``null`` on a
            nullable field clears it.

            Unknown keys are intentionally tolerated (``extra='ignore'``, the
            Pydantic default) so a rolling deploy stays safe: during the window
            between an API rollout that adds a new metadata field and the
            matching dashboard rollout, a dashboard PATCH that still sends an
            older shape (or, in the reverse direction, a dashboard that already
            sends a newer field name) must not 422 the curator out of a save.
            The trade-off is that a typo in a hand-rolled curator script
            silently no-ops the misspelled key; the dashboard form is the only
            real client and is exercised end-to-end before each deploy.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | VoiceCatalogEntry]
    """

    kwargs = _get_kwargs(
        voice_key=voice_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    voice_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: VoiceMetadataUpdate,
) -> HTTPValidationError | VoiceCatalogEntry | None:
    r"""Update Voice Metadata

     Update curator-editable fields on a global voice.

    Editable fields (all optional; omit a key to leave it unchanged):

    * ``display_name`` — curator-authored override for the customer-
      facing voice name. ``null`` clears the override and the public
      ``name`` reverts to the migrated value.
    * ``status`` — soft-retire flag. ``\"active\"`` shows the voice on
      ``GET /voices``; ``\"retired\"`` hides it from listings and 404s
      ``GET /voices/{voice_id}`` while leaving the row (and the
      internal voice-registry consumed by the TTS pod) untouched.
    * ``description`` — customer-facing one-liner; ``null`` clears.
      Brand-leak validated like ``display_name``.
    * ``internal_notes`` — admin-only commentary, never copied onto the
      public ``VoiceResponse``. ``null`` clears.
    * ``tags`` — closed-vocabulary list of tokens drawn from
      :data:`aethex.models.voice.VOICE_TAG_VOCABULARY`. ``[]`` clears;
      sending ``null`` is rejected because the column is NOT NULL.
    * ``gender`` — curator-authored correction for the speaker's
      perceived gender (``male`` / ``female`` / ``neutral``). The seed
      value is best-effort and known to be wrong on some pool voices.
      Sending ``null`` is rejected because the column is NOT NULL;
      an out-of-set value 422s with the field path.

    All flow through ``body.model_dump(exclude_unset=True)`` so a single
    PATCH can update any combination of fields.

    Scoped to ``tenant_id IS NULL`` (tenant-cloned voices are not
    editable through this endpoint). The ``Voice.public_name`` property
    is the single source of truth for the ``display_name or name``
    fallback chain so this endpoint and ``_voice_to_response`` cannot
    drift.

    Auth comes from the router-level ``X-Internal-Auth`` dependency.
    Unknown keys are silently dropped (``extra='ignore'``) so a rolling
    deploy that adds a new metadata field on the API side, or one that
    adds it on the dashboard side first, does not 422 the curator out
    of a save during the window where the two halves disagree on shape.
    The body schema still enforces oversize strings, any ``display_name``
    / ``description`` value that looks like an internal voice_key or
    carries a known brand-leak token, any ``status`` outside
    ``('active', 'retired')``, and any ``tags`` entry outside the
    closed vocabulary.

    Args:
        voice_key (str):
        body (VoiceMetadataUpdate): Body for ``PATCH /internal/voices/{voice_key}``.

            Editable fields:

            * ``display_name``: curator-authored override for the customer-facing
              voice name. The migrated ``name`` value is the durable fallback;
              setting this to ``null`` clears the override and the response reverts
              to the migrated name.
            * ``status``: soft-retire flag. ``"active"`` shows the voice on
              ``GET /voices``; ``"retired"`` hides it from listings and 404s
              ``GET /voices/{voice_id}`` while leaving the row (and the internal
              voice-registry consumed by the TTS pod) untouched.
            * ``description``: customer-facing one-liner. Brand-leak validated
              like ``display_name``.
            * ``internal_notes``: admin-only commentary, never copied onto the
              public ``VoiceResponse``. No brand-leak scrub because the field is
              meant to hold context that legitimately names internal voices.
            * ``tags``: closed-vocabulary list of tokens drawn from
              :data:`VOICE_TAG_VOCABULARY`. Send ``[]`` to clear; sending
              ``null`` is rejected because the underlying column is NOT NULL.
            * ``gender``: curator-authored correction for the speaker's perceived
              gender. The seed gender is best-effort and is known to be wrong on
              some pool voices, so the dashboard exposes a male/female/neutral
              selector that PATCHes the canonical value here. Sending ``null``
              is rejected because the underlying column is NOT NULL; omit the
              key to leave the existing value unchanged.

            Every field is optional. Omitting a key leaves the column untouched
            via ``model_dump(exclude_unset=True)``; sending ``null`` on a
            nullable field clears it.

            Unknown keys are intentionally tolerated (``extra='ignore'``, the
            Pydantic default) so a rolling deploy stays safe: during the window
            between an API rollout that adds a new metadata field and the
            matching dashboard rollout, a dashboard PATCH that still sends an
            older shape (or, in the reverse direction, a dashboard that already
            sends a newer field name) must not 422 the curator out of a save.
            The trade-off is that a typo in a hand-rolled curator script
            silently no-ops the misspelled key; the dashboard form is the only
            real client and is exercised end-to-end before each deploy.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | VoiceCatalogEntry
    """

    return sync_detailed(
        voice_key=voice_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    voice_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: VoiceMetadataUpdate,
) -> Response[HTTPValidationError | VoiceCatalogEntry]:
    r"""Update Voice Metadata

     Update curator-editable fields on a global voice.

    Editable fields (all optional; omit a key to leave it unchanged):

    * ``display_name`` — curator-authored override for the customer-
      facing voice name. ``null`` clears the override and the public
      ``name`` reverts to the migrated value.
    * ``status`` — soft-retire flag. ``\"active\"`` shows the voice on
      ``GET /voices``; ``\"retired\"`` hides it from listings and 404s
      ``GET /voices/{voice_id}`` while leaving the row (and the
      internal voice-registry consumed by the TTS pod) untouched.
    * ``description`` — customer-facing one-liner; ``null`` clears.
      Brand-leak validated like ``display_name``.
    * ``internal_notes`` — admin-only commentary, never copied onto the
      public ``VoiceResponse``. ``null`` clears.
    * ``tags`` — closed-vocabulary list of tokens drawn from
      :data:`aethex.models.voice.VOICE_TAG_VOCABULARY`. ``[]`` clears;
      sending ``null`` is rejected because the column is NOT NULL.
    * ``gender`` — curator-authored correction for the speaker's
      perceived gender (``male`` / ``female`` / ``neutral``). The seed
      value is best-effort and known to be wrong on some pool voices.
      Sending ``null`` is rejected because the column is NOT NULL;
      an out-of-set value 422s with the field path.

    All flow through ``body.model_dump(exclude_unset=True)`` so a single
    PATCH can update any combination of fields.

    Scoped to ``tenant_id IS NULL`` (tenant-cloned voices are not
    editable through this endpoint). The ``Voice.public_name`` property
    is the single source of truth for the ``display_name or name``
    fallback chain so this endpoint and ``_voice_to_response`` cannot
    drift.

    Auth comes from the router-level ``X-Internal-Auth`` dependency.
    Unknown keys are silently dropped (``extra='ignore'``) so a rolling
    deploy that adds a new metadata field on the API side, or one that
    adds it on the dashboard side first, does not 422 the curator out
    of a save during the window where the two halves disagree on shape.
    The body schema still enforces oversize strings, any ``display_name``
    / ``description`` value that looks like an internal voice_key or
    carries a known brand-leak token, any ``status`` outside
    ``('active', 'retired')``, and any ``tags`` entry outside the
    closed vocabulary.

    Args:
        voice_key (str):
        body (VoiceMetadataUpdate): Body for ``PATCH /internal/voices/{voice_key}``.

            Editable fields:

            * ``display_name``: curator-authored override for the customer-facing
              voice name. The migrated ``name`` value is the durable fallback;
              setting this to ``null`` clears the override and the response reverts
              to the migrated name.
            * ``status``: soft-retire flag. ``"active"`` shows the voice on
              ``GET /voices``; ``"retired"`` hides it from listings and 404s
              ``GET /voices/{voice_id}`` while leaving the row (and the internal
              voice-registry consumed by the TTS pod) untouched.
            * ``description``: customer-facing one-liner. Brand-leak validated
              like ``display_name``.
            * ``internal_notes``: admin-only commentary, never copied onto the
              public ``VoiceResponse``. No brand-leak scrub because the field is
              meant to hold context that legitimately names internal voices.
            * ``tags``: closed-vocabulary list of tokens drawn from
              :data:`VOICE_TAG_VOCABULARY`. Send ``[]`` to clear; sending
              ``null`` is rejected because the underlying column is NOT NULL.
            * ``gender``: curator-authored correction for the speaker's perceived
              gender. The seed gender is best-effort and is known to be wrong on
              some pool voices, so the dashboard exposes a male/female/neutral
              selector that PATCHes the canonical value here. Sending ``null``
              is rejected because the underlying column is NOT NULL; omit the
              key to leave the existing value unchanged.

            Every field is optional. Omitting a key leaves the column untouched
            via ``model_dump(exclude_unset=True)``; sending ``null`` on a
            nullable field clears it.

            Unknown keys are intentionally tolerated (``extra='ignore'``, the
            Pydantic default) so a rolling deploy stays safe: during the window
            between an API rollout that adds a new metadata field and the
            matching dashboard rollout, a dashboard PATCH that still sends an
            older shape (or, in the reverse direction, a dashboard that already
            sends a newer field name) must not 422 the curator out of a save.
            The trade-off is that a typo in a hand-rolled curator script
            silently no-ops the misspelled key; the dashboard form is the only
            real client and is exercised end-to-end before each deploy.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | VoiceCatalogEntry]
    """

    kwargs = _get_kwargs(
        voice_key=voice_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    voice_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: VoiceMetadataUpdate,
) -> HTTPValidationError | VoiceCatalogEntry | None:
    r"""Update Voice Metadata

     Update curator-editable fields on a global voice.

    Editable fields (all optional; omit a key to leave it unchanged):

    * ``display_name`` — curator-authored override for the customer-
      facing voice name. ``null`` clears the override and the public
      ``name`` reverts to the migrated value.
    * ``status`` — soft-retire flag. ``\"active\"`` shows the voice on
      ``GET /voices``; ``\"retired\"`` hides it from listings and 404s
      ``GET /voices/{voice_id}`` while leaving the row (and the
      internal voice-registry consumed by the TTS pod) untouched.
    * ``description`` — customer-facing one-liner; ``null`` clears.
      Brand-leak validated like ``display_name``.
    * ``internal_notes`` — admin-only commentary, never copied onto the
      public ``VoiceResponse``. ``null`` clears.
    * ``tags`` — closed-vocabulary list of tokens drawn from
      :data:`aethex.models.voice.VOICE_TAG_VOCABULARY`. ``[]`` clears;
      sending ``null`` is rejected because the column is NOT NULL.
    * ``gender`` — curator-authored correction for the speaker's
      perceived gender (``male`` / ``female`` / ``neutral``). The seed
      value is best-effort and known to be wrong on some pool voices.
      Sending ``null`` is rejected because the column is NOT NULL;
      an out-of-set value 422s with the field path.

    All flow through ``body.model_dump(exclude_unset=True)`` so a single
    PATCH can update any combination of fields.

    Scoped to ``tenant_id IS NULL`` (tenant-cloned voices are not
    editable through this endpoint). The ``Voice.public_name`` property
    is the single source of truth for the ``display_name or name``
    fallback chain so this endpoint and ``_voice_to_response`` cannot
    drift.

    Auth comes from the router-level ``X-Internal-Auth`` dependency.
    Unknown keys are silently dropped (``extra='ignore'``) so a rolling
    deploy that adds a new metadata field on the API side, or one that
    adds it on the dashboard side first, does not 422 the curator out
    of a save during the window where the two halves disagree on shape.
    The body schema still enforces oversize strings, any ``display_name``
    / ``description`` value that looks like an internal voice_key or
    carries a known brand-leak token, any ``status`` outside
    ``('active', 'retired')``, and any ``tags`` entry outside the
    closed vocabulary.

    Args:
        voice_key (str):
        body (VoiceMetadataUpdate): Body for ``PATCH /internal/voices/{voice_key}``.

            Editable fields:

            * ``display_name``: curator-authored override for the customer-facing
              voice name. The migrated ``name`` value is the durable fallback;
              setting this to ``null`` clears the override and the response reverts
              to the migrated name.
            * ``status``: soft-retire flag. ``"active"`` shows the voice on
              ``GET /voices``; ``"retired"`` hides it from listings and 404s
              ``GET /voices/{voice_id}`` while leaving the row (and the internal
              voice-registry consumed by the TTS pod) untouched.
            * ``description``: customer-facing one-liner. Brand-leak validated
              like ``display_name``.
            * ``internal_notes``: admin-only commentary, never copied onto the
              public ``VoiceResponse``. No brand-leak scrub because the field is
              meant to hold context that legitimately names internal voices.
            * ``tags``: closed-vocabulary list of tokens drawn from
              :data:`VOICE_TAG_VOCABULARY`. Send ``[]`` to clear; sending
              ``null`` is rejected because the underlying column is NOT NULL.
            * ``gender``: curator-authored correction for the speaker's perceived
              gender. The seed gender is best-effort and is known to be wrong on
              some pool voices, so the dashboard exposes a male/female/neutral
              selector that PATCHes the canonical value here. Sending ``null``
              is rejected because the underlying column is NOT NULL; omit the
              key to leave the existing value unchanged.

            Every field is optional. Omitting a key leaves the column untouched
            via ``model_dump(exclude_unset=True)``; sending ``null`` on a
            nullable field clears it.

            Unknown keys are intentionally tolerated (``extra='ignore'``, the
            Pydantic default) so a rolling deploy stays safe: during the window
            between an API rollout that adds a new metadata field and the
            matching dashboard rollout, a dashboard PATCH that still sends an
            older shape (or, in the reverse direction, a dashboard that already
            sends a newer field name) must not 422 the curator out of a save.
            The trade-off is that a typo in a hand-rolled curator script
            silently no-ops the misspelled key; the dashboard form is the only
            real client and is exercised end-to-end before each deploy.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | VoiceCatalogEntry
    """

    return (
        await asyncio_detailed(
            voice_key=voice_key,
            client=client,
            body=body,
        )
    ).parsed
