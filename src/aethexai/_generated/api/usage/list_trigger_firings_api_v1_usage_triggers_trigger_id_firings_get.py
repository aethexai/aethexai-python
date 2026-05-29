from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.usage_trigger_firing_response import UsageTriggerFiringResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID


def _get_kwargs(
    trigger_id: UUID,
    *,
    limit: int | Unset = 50,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/usage/triggers/{trigger_id}/firings".format(
            trigger_id=quote(str(trigger_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[UsageTriggerFiringResponse] | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UsageTriggerFiringResponse.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[UsageTriggerFiringResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    trigger_id: UUID,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
) -> Response[HTTPValidationError | list[UsageTriggerFiringResponse]]:
    """List Trigger Firings

     Audit log for a single trigger's firing attempts. Newest-first. ``limit`` is enforced 1..200 by
    Pydantic; values
    outside that range 422 at the boundary. Returns 404 if the trigger
    isn't owned by the calling tenant so a customer can't probe other
    tenants' trigger ids by guessing.

    Args:
        trigger_id (UUID):
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[UsageTriggerFiringResponse]]
    """

    kwargs = _get_kwargs(
        trigger_id=trigger_id,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    trigger_id: UUID,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
) -> HTTPValidationError | list[UsageTriggerFiringResponse] | None:
    """List Trigger Firings

     Audit log for a single trigger's firing attempts. Newest-first. ``limit`` is enforced 1..200 by
    Pydantic; values
    outside that range 422 at the boundary. Returns 404 if the trigger
    isn't owned by the calling tenant so a customer can't probe other
    tenants' trigger ids by guessing.

    Args:
        trigger_id (UUID):
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[UsageTriggerFiringResponse]
    """

    return sync_detailed(
        trigger_id=trigger_id,
        client=client,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    trigger_id: UUID,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
) -> Response[HTTPValidationError | list[UsageTriggerFiringResponse]]:
    """List Trigger Firings

     Audit log for a single trigger's firing attempts. Newest-first. ``limit`` is enforced 1..200 by
    Pydantic; values
    outside that range 422 at the boundary. Returns 404 if the trigger
    isn't owned by the calling tenant so a customer can't probe other
    tenants' trigger ids by guessing.

    Args:
        trigger_id (UUID):
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[UsageTriggerFiringResponse]]
    """

    kwargs = _get_kwargs(
        trigger_id=trigger_id,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    trigger_id: UUID,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
) -> HTTPValidationError | list[UsageTriggerFiringResponse] | None:
    """List Trigger Firings

     Audit log for a single trigger's firing attempts. Newest-first. ``limit`` is enforced 1..200 by
    Pydantic; values
    outside that range 422 at the boundary. Returns 404 if the trigger
    isn't owned by the calling tenant so a customer can't probe other
    tenants' trigger ids by guessing.

    Args:
        trigger_id (UUID):
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[UsageTriggerFiringResponse]
    """

    return (
        await asyncio_detailed(
            trigger_id=trigger_id,
            client=client,
            limit=limit,
        )
    ).parsed
