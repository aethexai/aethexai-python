from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.sip_trunk_response import SipTrunkResponse
from ...models.sip_trunk_update import SipTrunkUpdate
from typing import cast
from uuid import UUID


def _get_kwargs(
    trunk_id: UUID,
    *,
    body: SipTrunkUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/sip-trunks/{trunk_id}".format(
            trunk_id=quote(str(trunk_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | SipTrunkResponse | None:
    if response.status_code == 200:
        response_200 = SipTrunkResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | SipTrunkResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    trunk_id: UUID,
    *,
    client: AuthenticatedClient,
    body: SipTrunkUpdate,
) -> Response[HTTPValidationError | SipTrunkResponse]:
    """Update Sip Trunk

     Update a trunk's aethex-side policy fields and sync carrier-visible
    fields to LiveKit.

    Aethex-only fields (no LK sync needed): `destination_allowlist`,
    `max_concurrent_calls`, `calls_per_hour_limit`, `status`.

    LK-synced fields (must be replicated): `numbers`, `allowed_addresses`.
    For outbound trunks, changing `numbers` requires creating a new trunk
    (the LK SDK's UpdateSIPOutboundTrunk doesn't expose that field); we
    reject the change with a 422 and point to the runbook rotation flow.
    Changing `auth_mode` also requires replacement because the digest
    password is intentionally not persisted in Aethex.

    Args:
        trunk_id (UUID):
        body (SipTrunkUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SipTrunkResponse]
    """

    kwargs = _get_kwargs(
        trunk_id=trunk_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    trunk_id: UUID,
    *,
    client: AuthenticatedClient,
    body: SipTrunkUpdate,
) -> HTTPValidationError | SipTrunkResponse | None:
    """Update Sip Trunk

     Update a trunk's aethex-side policy fields and sync carrier-visible
    fields to LiveKit.

    Aethex-only fields (no LK sync needed): `destination_allowlist`,
    `max_concurrent_calls`, `calls_per_hour_limit`, `status`.

    LK-synced fields (must be replicated): `numbers`, `allowed_addresses`.
    For outbound trunks, changing `numbers` requires creating a new trunk
    (the LK SDK's UpdateSIPOutboundTrunk doesn't expose that field); we
    reject the change with a 422 and point to the runbook rotation flow.
    Changing `auth_mode` also requires replacement because the digest
    password is intentionally not persisted in Aethex.

    Args:
        trunk_id (UUID):
        body (SipTrunkUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SipTrunkResponse
    """

    return sync_detailed(
        trunk_id=trunk_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    trunk_id: UUID,
    *,
    client: AuthenticatedClient,
    body: SipTrunkUpdate,
) -> Response[HTTPValidationError | SipTrunkResponse]:
    """Update Sip Trunk

     Update a trunk's aethex-side policy fields and sync carrier-visible
    fields to LiveKit.

    Aethex-only fields (no LK sync needed): `destination_allowlist`,
    `max_concurrent_calls`, `calls_per_hour_limit`, `status`.

    LK-synced fields (must be replicated): `numbers`, `allowed_addresses`.
    For outbound trunks, changing `numbers` requires creating a new trunk
    (the LK SDK's UpdateSIPOutboundTrunk doesn't expose that field); we
    reject the change with a 422 and point to the runbook rotation flow.
    Changing `auth_mode` also requires replacement because the digest
    password is intentionally not persisted in Aethex.

    Args:
        trunk_id (UUID):
        body (SipTrunkUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SipTrunkResponse]
    """

    kwargs = _get_kwargs(
        trunk_id=trunk_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    trunk_id: UUID,
    *,
    client: AuthenticatedClient,
    body: SipTrunkUpdate,
) -> HTTPValidationError | SipTrunkResponse | None:
    """Update Sip Trunk

     Update a trunk's aethex-side policy fields and sync carrier-visible
    fields to LiveKit.

    Aethex-only fields (no LK sync needed): `destination_allowlist`,
    `max_concurrent_calls`, `calls_per_hour_limit`, `status`.

    LK-synced fields (must be replicated): `numbers`, `allowed_addresses`.
    For outbound trunks, changing `numbers` requires creating a new trunk
    (the LK SDK's UpdateSIPOutboundTrunk doesn't expose that field); we
    reject the change with a 422 and point to the runbook rotation flow.
    Changing `auth_mode` also requires replacement because the digest
    password is intentionally not persisted in Aethex.

    Args:
        trunk_id (UUID):
        body (SipTrunkUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SipTrunkResponse
    """

    return (
        await asyncio_detailed(
            trunk_id=trunk_id,
            client=client,
            body=body,
        )
    ).parsed
