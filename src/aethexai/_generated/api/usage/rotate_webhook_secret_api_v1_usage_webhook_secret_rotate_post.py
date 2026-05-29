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
    if response.status_code == 200:
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

     Generate (or replace) the tenant-level webhook signing secret. Tenant-owned webhook bodies are
    signed with this secret via
    HMAC-SHA256 (``X-Aethex-Signature`` header). This includes usage
    triggers, async transcription callbacks, and TTS batch callbacks. The secret is returned exactly
    once — store it securely. Rotating
    replaces it immediately; in-flight deliveries signed with the old
    secret will fail HMAC verification on the receiver side until you
    update your handler. A tenant that has never called this endpoint has no signing secret;
    the trigger evaluator records those firings as ``failed`` with
    ``last_error='tenant has no webhook_secret configured'``. Concurrency: the tenant row is locked with
    ``SELECT... FOR UPDATE``
    for the duration of this transaction so two simultaneous rotate
    calls serialise. Without the lock both callers could read the same
    pre-state, generate different new secrets, and only the last
    commit's secret would persist — the earlier caller would walk
    away with a secret that is already invalid and every webhook
    delivery to them would HMAC-mismatch.

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

     Generate (or replace) the tenant-level webhook signing secret. Tenant-owned webhook bodies are
    signed with this secret via
    HMAC-SHA256 (``X-Aethex-Signature`` header). This includes usage
    triggers, async transcription callbacks, and TTS batch callbacks. The secret is returned exactly
    once — store it securely. Rotating
    replaces it immediately; in-flight deliveries signed with the old
    secret will fail HMAC verification on the receiver side until you
    update your handler. A tenant that has never called this endpoint has no signing secret;
    the trigger evaluator records those firings as ``failed`` with
    ``last_error='tenant has no webhook_secret configured'``. Concurrency: the tenant row is locked with
    ``SELECT... FOR UPDATE``
    for the duration of this transaction so two simultaneous rotate
    calls serialise. Without the lock both callers could read the same
    pre-state, generate different new secrets, and only the last
    commit's secret would persist — the earlier caller would walk
    away with a secret that is already invalid and every webhook
    delivery to them would HMAC-mismatch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
