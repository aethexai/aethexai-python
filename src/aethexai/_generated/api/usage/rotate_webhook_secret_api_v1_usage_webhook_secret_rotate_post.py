from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/usage/webhook-secret/rotate",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    """Rotate Webhook Secret

     Generate (or replace) the tenant-level webhook signing secret. Webhook bodies — usage triggers,
    async transcription callbacks, and TTS batch callbacks — are signed with this secret via HMAC-SHA256
    (``X-Aethex-Signature`` header). The secret is returned exactly once — store it securely. Rotation
    takes effect immediately; in-flight deliveries signed with the old secret will fail HMAC
    verification on your receiver until you update your handler. Until you first call this endpoint the
    tenant has no signing secret, so usage-trigger firings are recorded as ``failed`` until one is
    configured. Concurrent rotate calls are serialized, so exactly one new secret takes effect.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    """Rotate Webhook Secret

     Generate (or replace) the tenant-level webhook signing secret. Webhook bodies — usage triggers,
    async transcription callbacks, and TTS batch callbacks — are signed with this secret via HMAC-SHA256
    (``X-Aethex-Signature`` header). The secret is returned exactly once — store it securely. Rotation
    takes effect immediately; in-flight deliveries signed with the old secret will fail HMAC
    verification on your receiver until you update your handler. Until you first call this endpoint the
    tenant has no signing secret, so usage-trigger firings are recorded as ``failed`` until one is
    configured. Concurrent rotate calls are serialized, so exactly one new secret takes effect.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
