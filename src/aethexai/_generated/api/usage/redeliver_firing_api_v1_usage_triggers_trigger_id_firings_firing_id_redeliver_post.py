from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.usage_trigger_firing_response import UsageTriggerFiringResponse
from typing import cast
from uuid import UUID


def _get_kwargs(
    trigger_id: UUID,
    firing_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/usage/triggers/{trigger_id}/firings/{firing_id}/redeliver".format(
            trigger_id=quote(str(trigger_id), safe=""),
            firing_id=quote(str(firing_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | UsageTriggerFiringResponse | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = UsageTriggerFiringResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | UsageTriggerFiringResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    trigger_id: UUID,
    firing_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | UsageTriggerFiringResponse]:
    """Redeliver Firing

     Re-attempt webhook delivery for a single firing. Replays the exact bytes originally sent so your
    receiver sees an identical signature and payload, updating the same firing in place (its
    ``attempt_count``, ``delivery_status``, ``http_status``, and ``last_error``) rather than recording a
    new firing. Returns 404 when the trigger or firing isn't owned by the calling tenant. Returns 400
    when the tenant has rotated their webhook_secret and the original signature would no longer verify,
    since the receiver would reject the replay as tampered; in that case configure a new trigger or wait
    for the next natural fire, which will use the new secret.

    Args:
        trigger_id (UUID):
        firing_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsageTriggerFiringResponse]
    """

    kwargs = _get_kwargs(
        trigger_id=trigger_id,
        firing_id=firing_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    trigger_id: UUID,
    firing_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | UsageTriggerFiringResponse | None:
    """Redeliver Firing

     Re-attempt webhook delivery for a single firing. Replays the exact bytes originally sent so your
    receiver sees an identical signature and payload, updating the same firing in place (its
    ``attempt_count``, ``delivery_status``, ``http_status``, and ``last_error``) rather than recording a
    new firing. Returns 404 when the trigger or firing isn't owned by the calling tenant. Returns 400
    when the tenant has rotated their webhook_secret and the original signature would no longer verify,
    since the receiver would reject the replay as tampered; in that case configure a new trigger or wait
    for the next natural fire, which will use the new secret.

    Args:
        trigger_id (UUID):
        firing_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsageTriggerFiringResponse
    """

    return sync_detailed(
        trigger_id=trigger_id,
        firing_id=firing_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    trigger_id: UUID,
    firing_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | UsageTriggerFiringResponse]:
    """Redeliver Firing

     Re-attempt webhook delivery for a single firing. Replays the exact bytes originally sent so your
    receiver sees an identical signature and payload, updating the same firing in place (its
    ``attempt_count``, ``delivery_status``, ``http_status``, and ``last_error``) rather than recording a
    new firing. Returns 404 when the trigger or firing isn't owned by the calling tenant. Returns 400
    when the tenant has rotated their webhook_secret and the original signature would no longer verify,
    since the receiver would reject the replay as tampered; in that case configure a new trigger or wait
    for the next natural fire, which will use the new secret.

    Args:
        trigger_id (UUID):
        firing_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsageTriggerFiringResponse]
    """

    kwargs = _get_kwargs(
        trigger_id=trigger_id,
        firing_id=firing_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    trigger_id: UUID,
    firing_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | UsageTriggerFiringResponse | None:
    """Redeliver Firing

     Re-attempt webhook delivery for a single firing. Replays the exact bytes originally sent so your
    receiver sees an identical signature and payload, updating the same firing in place (its
    ``attempt_count``, ``delivery_status``, ``http_status``, and ``last_error``) rather than recording a
    new firing. Returns 404 when the trigger or firing isn't owned by the calling tenant. Returns 400
    when the tenant has rotated their webhook_secret and the original signature would no longer verify,
    since the receiver would reject the replay as tampered; in that case configure a new trigger or wait
    for the next natural fire, which will use the new secret.

    Args:
        trigger_id (UUID):
        firing_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsageTriggerFiringResponse
    """

    return (
        await asyncio_detailed(
            trigger_id=trigger_id,
            firing_id=firing_id,
            client=client,
        )
    ).parsed
