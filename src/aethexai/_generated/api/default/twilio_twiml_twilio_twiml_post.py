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
    agent_id: str | Unset = UNSET,
    inbound_lobby_elapsed_seconds: int | Unset = 0,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["agent_id"] = agent_id

    params["inbound_lobby_elapsed_seconds"] = inbound_lobby_elapsed_seconds

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/twilio/twiml",
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
    agent_id: str | Unset = UNSET,
    inbound_lobby_elapsed_seconds: int | Unset = 0,
) -> Response[Any | HTTPValidationError]:
    """Twilio Twiml

     TwiML webhook for inbound calls — loads agent config and streams to /twilio/ws.

    First hit (``inbound_lobby_elapsed_seconds == 0``) loads the agent from
    the DB and writes the config to Redis. Lobby redirects read the cached
    config from Redis so each cycle costs one Redis GET instead of a DB query
    plus a Redis SET. Langfuse prefetch is also fired only on the first hit.

    Twilio request signature is verified before we touch the DB. Without
    this, anyone with the public webhook URL could POST a forged CallSid
    + agent_id and pollute ``vo_calls`` / ``vo_conversations``.

    Args:
        agent_id (str | Unset):
        inbound_lobby_elapsed_seconds (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        agent_id=agent_id,
        inbound_lobby_elapsed_seconds=inbound_lobby_elapsed_seconds,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    inbound_lobby_elapsed_seconds: int | Unset = 0,
) -> Any | HTTPValidationError | None:
    """Twilio Twiml

     TwiML webhook for inbound calls — loads agent config and streams to /twilio/ws.

    First hit (``inbound_lobby_elapsed_seconds == 0``) loads the agent from
    the DB and writes the config to Redis. Lobby redirects read the cached
    config from Redis so each cycle costs one Redis GET instead of a DB query
    plus a Redis SET. Langfuse prefetch is also fired only on the first hit.

    Twilio request signature is verified before we touch the DB. Without
    this, anyone with the public webhook URL could POST a forged CallSid
    + agent_id and pollute ``vo_calls`` / ``vo_conversations``.

    Args:
        agent_id (str | Unset):
        inbound_lobby_elapsed_seconds (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        agent_id=agent_id,
        inbound_lobby_elapsed_seconds=inbound_lobby_elapsed_seconds,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    inbound_lobby_elapsed_seconds: int | Unset = 0,
) -> Response[Any | HTTPValidationError]:
    """Twilio Twiml

     TwiML webhook for inbound calls — loads agent config and streams to /twilio/ws.

    First hit (``inbound_lobby_elapsed_seconds == 0``) loads the agent from
    the DB and writes the config to Redis. Lobby redirects read the cached
    config from Redis so each cycle costs one Redis GET instead of a DB query
    plus a Redis SET. Langfuse prefetch is also fired only on the first hit.

    Twilio request signature is verified before we touch the DB. Without
    this, anyone with the public webhook URL could POST a forged CallSid
    + agent_id and pollute ``vo_calls`` / ``vo_conversations``.

    Args:
        agent_id (str | Unset):
        inbound_lobby_elapsed_seconds (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        agent_id=agent_id,
        inbound_lobby_elapsed_seconds=inbound_lobby_elapsed_seconds,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    inbound_lobby_elapsed_seconds: int | Unset = 0,
) -> Any | HTTPValidationError | None:
    """Twilio Twiml

     TwiML webhook for inbound calls — loads agent config and streams to /twilio/ws.

    First hit (``inbound_lobby_elapsed_seconds == 0``) loads the agent from
    the DB and writes the config to Redis. Lobby redirects read the cached
    config from Redis so each cycle costs one Redis GET instead of a DB query
    plus a Redis SET. Langfuse prefetch is also fired only on the first hit.

    Twilio request signature is verified before we touch the DB. Without
    this, anyone with the public webhook URL could POST a forged CallSid
    + agent_id and pollute ``vo_calls`` / ``vo_conversations``.

    Args:
        agent_id (str | Unset):
        inbound_lobby_elapsed_seconds (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            agent_id=agent_id,
            inbound_lobby_elapsed_seconds=inbound_lobby_elapsed_seconds,
        )
    ).parsed
