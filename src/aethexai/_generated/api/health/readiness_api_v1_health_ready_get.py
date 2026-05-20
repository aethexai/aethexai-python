from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/health/ready",
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
    client: AuthenticatedClient | Client,
) -> Response[Any]:
    """Readiness

     Readiness probe.

    Returns 503 when any of these gates are closed:
    - ``app.state.shutting_down`` is True (preStop drain)
    - ``app.state.langfuse_prompts_warmed`` is False (initial prompt prefetch
      still in flight)
    - DB SELECT 1 fails
    - Redis is configured but unreachable

    Provider health is intentionally not a readiness gate. External ML
    services (ASR/TTS/LLM) may take minutes to come up, and the TTS pods fetch
    their DB-backed voice registry through this app Service during startup. If
    app readiness waits on TTS readiness, a rollout can deadlock with no ready
    app Service endpoints for TTS to call.

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
    client: AuthenticatedClient | Client,
) -> Response[Any]:
    """Readiness

     Readiness probe.

    Returns 503 when any of these gates are closed:
    - ``app.state.shutting_down`` is True (preStop drain)
    - ``app.state.langfuse_prompts_warmed`` is False (initial prompt prefetch
      still in flight)
    - DB SELECT 1 fails
    - Redis is configured but unreachable

    Provider health is intentionally not a readiness gate. External ML
    services (ASR/TTS/LLM) may take minutes to come up, and the TTS pods fetch
    their DB-backed voice registry through this app Service during startup. If
    app readiness waits on TTS readiness, a rollout can deadlock with no ready
    app Service endpoints for TTS to call.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
