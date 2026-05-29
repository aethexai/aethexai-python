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
    if response.status_code == 200:
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
    r"""Redeliver Firing

     Re-attempt webhook delivery for a single firing. Replays the EXACT bytes we POSTed the first time so
    the receiver
    sees identical signature + payload. Updates the same audit row
    in place (incrementing ``attempt_count``, refreshing
    ``delivery_status`` / ``http_status`` / ``last_error``); we do
    NOT insert a new firing row because each row represents one
    \"threshold crossed for this period\" event and a redeliver is the
    same logical event, just retried. 404 when trigger or firing isn't owned by the calling tenant
    (no cross-tenant probing). 400 when the tenant has rotated their webhook_secret and the old
    signature would no longer verify on the receiver — refuse the
    redeliver because the receiver would silently reject it as
    tampered. Customer recovery: configure a new trigger or wait for
    the next natural fire (which will use the new secret).

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
    r"""Redeliver Firing

     Re-attempt webhook delivery for a single firing. Replays the EXACT bytes we POSTed the first time so
    the receiver
    sees identical signature + payload. Updates the same audit row
    in place (incrementing ``attempt_count``, refreshing
    ``delivery_status`` / ``http_status`` / ``last_error``); we do
    NOT insert a new firing row because each row represents one
    \"threshold crossed for this period\" event and a redeliver is the
    same logical event, just retried. 404 when trigger or firing isn't owned by the calling tenant
    (no cross-tenant probing). 400 when the tenant has rotated their webhook_secret and the old
    signature would no longer verify on the receiver — refuse the
    redeliver because the receiver would silently reject it as
    tampered. Customer recovery: configure a new trigger or wait for
    the next natural fire (which will use the new secret).

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
    r"""Redeliver Firing

     Re-attempt webhook delivery for a single firing. Replays the EXACT bytes we POSTed the first time so
    the receiver
    sees identical signature + payload. Updates the same audit row
    in place (incrementing ``attempt_count``, refreshing
    ``delivery_status`` / ``http_status`` / ``last_error``); we do
    NOT insert a new firing row because each row represents one
    \"threshold crossed for this period\" event and a redeliver is the
    same logical event, just retried. 404 when trigger or firing isn't owned by the calling tenant
    (no cross-tenant probing). 400 when the tenant has rotated their webhook_secret and the old
    signature would no longer verify on the receiver — refuse the
    redeliver because the receiver would silently reject it as
    tampered. Customer recovery: configure a new trigger or wait for
    the next natural fire (which will use the new secret).

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
    r"""Redeliver Firing

     Re-attempt webhook delivery for a single firing. Replays the EXACT bytes we POSTed the first time so
    the receiver
    sees identical signature + payload. Updates the same audit row
    in place (incrementing ``attempt_count``, refreshing
    ``delivery_status`` / ``http_status`` / ``last_error``); we do
    NOT insert a new firing row because each row represents one
    \"threshold crossed for this period\" event and a redeliver is the
    same logical event, just retried. 404 when trigger or firing isn't owned by the calling tenant
    (no cross-tenant probing). 400 when the tenant has rotated their webhook_secret and the old
    signature would no longer verify on the receiver — refuse the
    redeliver because the receiver would silently reject it as
    tampered. Customer recovery: configure a new trigger or wait for
    the next natural fire (which will use the new secret).

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
