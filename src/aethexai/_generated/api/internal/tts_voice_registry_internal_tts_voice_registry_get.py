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


def _get_kwargs(
    *,
    endpoint: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_endpoint: None | str | Unset
    if isinstance(endpoint, Unset):
        json_endpoint = UNSET
    else:
        json_endpoint = endpoint
    params["endpoint"] = json_endpoint

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/internal/tts/voice-registry",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
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
    *,
    client: AuthenticatedClient | Client,
    endpoint: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Tts Voice Registry

     Return the ICL voice catalog for loading into a TTS pod.

    Rows returned:
      - ``tenant_id IS NULL`` (global catalog only, no tenant-cloned voices).
        Tenant-cloned voices are served via a separate per-tenant flow.
      - ``ref_audio_key IS NOT NULL`` (voice is actually serviceable —
        orphan rows with no ref audio pointer are excluded).
      - If ``endpoint`` is provided, only voices routed to a ``TtsModel``
        with a matching endpoint are returned.

    Fine-tuned voices have ``ref_audio_key=NULL`` and are therefore
    excluded — correct, since FT pods serve their baked-in identity
    regardless of speaker input and don't need ICL references loaded.

    Response shape::

        {
          \"voices\": [
            {\"voice_key\": \"adaeze\", \"ref_audio_key\": \"adaeze_ref.wav\",
             \"ref_text\": null, \"gender\": \"female\", \"language\": \"nigerian_english\"},
            {\"voice_key\": \"ci-aminata\", \"ref_audio_key\": \"awa_ref.wav\",
             \"ref_text\": null, \"gender\": \"female\", \"language\": \"ivorian_french\"},
            ...
          ]
        }

    Args:
        endpoint (None | str | Unset): If provided, only return voices whose TtsModel.endpoint
            matches this URL. Used by TTS pods to ask 'what voices should I serve?' If omitted,
            returns every global ICL voice that has ref audio.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        endpoint=endpoint,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    endpoint: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Tts Voice Registry

     Return the ICL voice catalog for loading into a TTS pod.

    Rows returned:
      - ``tenant_id IS NULL`` (global catalog only, no tenant-cloned voices).
        Tenant-cloned voices are served via a separate per-tenant flow.
      - ``ref_audio_key IS NOT NULL`` (voice is actually serviceable —
        orphan rows with no ref audio pointer are excluded).
      - If ``endpoint`` is provided, only voices routed to a ``TtsModel``
        with a matching endpoint are returned.

    Fine-tuned voices have ``ref_audio_key=NULL`` and are therefore
    excluded — correct, since FT pods serve their baked-in identity
    regardless of speaker input and don't need ICL references loaded.

    Response shape::

        {
          \"voices\": [
            {\"voice_key\": \"adaeze\", \"ref_audio_key\": \"adaeze_ref.wav\",
             \"ref_text\": null, \"gender\": \"female\", \"language\": \"nigerian_english\"},
            {\"voice_key\": \"ci-aminata\", \"ref_audio_key\": \"awa_ref.wav\",
             \"ref_text\": null, \"gender\": \"female\", \"language\": \"ivorian_french\"},
            ...
          ]
        }

    Args:
        endpoint (None | str | Unset): If provided, only return voices whose TtsModel.endpoint
            matches this URL. Used by TTS pods to ask 'what voices should I serve?' If omitted,
            returns every global ICL voice that has ref audio.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        endpoint=endpoint,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    endpoint: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Tts Voice Registry

     Return the ICL voice catalog for loading into a TTS pod.

    Rows returned:
      - ``tenant_id IS NULL`` (global catalog only, no tenant-cloned voices).
        Tenant-cloned voices are served via a separate per-tenant flow.
      - ``ref_audio_key IS NOT NULL`` (voice is actually serviceable —
        orphan rows with no ref audio pointer are excluded).
      - If ``endpoint`` is provided, only voices routed to a ``TtsModel``
        with a matching endpoint are returned.

    Fine-tuned voices have ``ref_audio_key=NULL`` and are therefore
    excluded — correct, since FT pods serve their baked-in identity
    regardless of speaker input and don't need ICL references loaded.

    Response shape::

        {
          \"voices\": [
            {\"voice_key\": \"adaeze\", \"ref_audio_key\": \"adaeze_ref.wav\",
             \"ref_text\": null, \"gender\": \"female\", \"language\": \"nigerian_english\"},
            {\"voice_key\": \"ci-aminata\", \"ref_audio_key\": \"awa_ref.wav\",
             \"ref_text\": null, \"gender\": \"female\", \"language\": \"ivorian_french\"},
            ...
          ]
        }

    Args:
        endpoint (None | str | Unset): If provided, only return voices whose TtsModel.endpoint
            matches this URL. Used by TTS pods to ask 'what voices should I serve?' If omitted,
            returns every global ICL voice that has ref audio.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        endpoint=endpoint,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    endpoint: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Tts Voice Registry

     Return the ICL voice catalog for loading into a TTS pod.

    Rows returned:
      - ``tenant_id IS NULL`` (global catalog only, no tenant-cloned voices).
        Tenant-cloned voices are served via a separate per-tenant flow.
      - ``ref_audio_key IS NOT NULL`` (voice is actually serviceable —
        orphan rows with no ref audio pointer are excluded).
      - If ``endpoint`` is provided, only voices routed to a ``TtsModel``
        with a matching endpoint are returned.

    Fine-tuned voices have ``ref_audio_key=NULL`` and are therefore
    excluded — correct, since FT pods serve their baked-in identity
    regardless of speaker input and don't need ICL references loaded.

    Response shape::

        {
          \"voices\": [
            {\"voice_key\": \"adaeze\", \"ref_audio_key\": \"adaeze_ref.wav\",
             \"ref_text\": null, \"gender\": \"female\", \"language\": \"nigerian_english\"},
            {\"voice_key\": \"ci-aminata\", \"ref_audio_key\": \"awa_ref.wav\",
             \"ref_text\": null, \"gender\": \"female\", \"language\": \"ivorian_french\"},
            ...
          ]
        }

    Args:
        endpoint (None | str | Unset): If provided, only return voices whose TtsModel.endpoint
            matches this URL. Used by TTS pods to ask 'what voices should I serve?' If omitted,
            returns every global ICL voice that has ref audio.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            endpoint=endpoint,
        )
    ).parsed
