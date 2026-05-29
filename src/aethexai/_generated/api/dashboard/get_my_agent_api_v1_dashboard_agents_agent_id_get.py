from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import cast
from uuid import UUID


def _get_kwargs(
    agent_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/dashboard/agents/{agent_id}".format(
            agent_id=quote(str(agent_id), safe=""),
        ),
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
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    r"""Get My Agent

     Fetch a small header view of a single agent for the developer's tenant. Distinct from ``GET
    /api/v1/agents/{id}`` (API-key-authed, full record):
    this JWT-authed variant returns only the fields the dashboard renders
    on the agent detail / Test surfaces. Pairs ``voice_id`` with the
    curator-authored display name from ```` so the page can show
    \"Adamma\" instead of an internal slug. Returns 404 if the agent doesn't
    exist or doesn't belong to the developer's tenant — same shape as the
    API-key endpoint so the portal can reuse its missing-agent rendering.

    Args:
        agent_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        agent_id=agent_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    r"""Get My Agent

     Fetch a small header view of a single agent for the developer's tenant. Distinct from ``GET
    /api/v1/agents/{id}`` (API-key-authed, full record):
    this JWT-authed variant returns only the fields the dashboard renders
    on the agent detail / Test surfaces. Pairs ``voice_id`` with the
    curator-authored display name from ```` so the page can show
    \"Adamma\" instead of an internal slug. Returns 404 if the agent doesn't
    exist or doesn't belong to the developer's tenant — same shape as the
    API-key endpoint so the portal can reuse its missing-agent rendering.

    Args:
        agent_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        agent_id=agent_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    r"""Get My Agent

     Fetch a small header view of a single agent for the developer's tenant. Distinct from ``GET
    /api/v1/agents/{id}`` (API-key-authed, full record):
    this JWT-authed variant returns only the fields the dashboard renders
    on the agent detail / Test surfaces. Pairs ``voice_id`` with the
    curator-authored display name from ```` so the page can show
    \"Adamma\" instead of an internal slug. Returns 404 if the agent doesn't
    exist or doesn't belong to the developer's tenant — same shape as the
    API-key endpoint so the portal can reuse its missing-agent rendering.

    Args:
        agent_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        agent_id=agent_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    r"""Get My Agent

     Fetch a small header view of a single agent for the developer's tenant. Distinct from ``GET
    /api/v1/agents/{id}`` (API-key-authed, full record):
    this JWT-authed variant returns only the fields the dashboard renders
    on the agent detail / Test surfaces. Pairs ``voice_id`` with the
    curator-authored display name from ```` so the page can show
    \"Adamma\" instead of an internal slug. Returns 404 if the agent doesn't
    exist or doesn't belong to the developer's tenant — same shape as the
    API-key endpoint so the portal can reuse its missing-agent rendering.

    Args:
        agent_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            agent_id=agent_id,
            client=client,
        )
    ).parsed
