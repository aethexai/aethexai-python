from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.usage_trigger_response import UsageTriggerResponse
from ...models.usage_trigger_update import UsageTriggerUpdate
from typing import cast
from uuid import UUID


def _get_kwargs(
    trigger_id: UUID,
    *,
    body: UsageTriggerUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/usage/triggers/{trigger_id}".format(
            trigger_id=quote(str(trigger_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | UsageTriggerResponse | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = UsageTriggerResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | UsageTriggerResponse]:
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
    body: UsageTriggerUpdate,
) -> Response[HTTPValidationError | UsageTriggerResponse]:
    """Update Trigger

     Update a trigger's mutable fields. Three fields are editable: ``is_active`` (deactivate to free a
    slot under the per-tenant cap), ``threshold_value`` (re-tune the trip point as your volume scales),
    and ``event_callback_url`` (change the receiver). The trigger shape — ``resource_type``,
    ``threshold_type``, ``period`` — is immutable; create a new trigger if you need a different shape.
    Returns 404 when the trigger doesn't exist or belongs to another tenant. Returns 400 when
    ``event_callback_url`` is structurally invalid or resolves to a non-public address; 503 when DNS
    resolution is unavailable. An empty body is a valid no-op. Activating (flipping ``is_active`` from
    false to true) re-checks the per-tenant active cap. Re-activating a trigger whose ``resource_type``
    is no longer a supported value returns 422 — create a new trigger with a currently-supported
    ``resource_type`` instead.

    Args:
        trigger_id (UUID):
        body (UsageTriggerUpdate): Partial update for ``PATCH /usage/triggers/{id}``. Only fields
            a customer can re-tune in place are exposed: the
            ``is_active`` flag (deactivate to recover the per-tenant cap
            without losing audit history), the threshold value (re-tune the
            trip point as their volume scales), and the callback URL (rotate
            the receiver). The trigger's *shape* — ``resource_type``,
            ``threshold_type``, ``period`` — is immutable; a different shape
            is logically a different trigger and should be created fresh so
            the firings audit table cleanly tracks one configuration over
            time. Every field is Optional; PATCH is partial. An empty body is a
            valid no-op. ``extra='forbid'`` rejects unknown keys with HTTP 422. This catches
            two real customer foot-guns at once: PATCHing an immutable shape
            field (``resource_type`` / ``threshold_type`` / ``period``) used
            to return 200 with the value silently dropped, and a misspelled
            editable field name (e.g. ``threshold_val``) used to return 200
            with no clue the change was ignored. Both now surface as an
            explicit validation error at the boundary.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsageTriggerResponse]
    """

    kwargs = _get_kwargs(
        trigger_id=trigger_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    trigger_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UsageTriggerUpdate,
) -> HTTPValidationError | UsageTriggerResponse | None:
    """Update Trigger

     Update a trigger's mutable fields. Three fields are editable: ``is_active`` (deactivate to free a
    slot under the per-tenant cap), ``threshold_value`` (re-tune the trip point as your volume scales),
    and ``event_callback_url`` (change the receiver). The trigger shape — ``resource_type``,
    ``threshold_type``, ``period`` — is immutable; create a new trigger if you need a different shape.
    Returns 404 when the trigger doesn't exist or belongs to another tenant. Returns 400 when
    ``event_callback_url`` is structurally invalid or resolves to a non-public address; 503 when DNS
    resolution is unavailable. An empty body is a valid no-op. Activating (flipping ``is_active`` from
    false to true) re-checks the per-tenant active cap. Re-activating a trigger whose ``resource_type``
    is no longer a supported value returns 422 — create a new trigger with a currently-supported
    ``resource_type`` instead.

    Args:
        trigger_id (UUID):
        body (UsageTriggerUpdate): Partial update for ``PATCH /usage/triggers/{id}``. Only fields
            a customer can re-tune in place are exposed: the
            ``is_active`` flag (deactivate to recover the per-tenant cap
            without losing audit history), the threshold value (re-tune the
            trip point as their volume scales), and the callback URL (rotate
            the receiver). The trigger's *shape* — ``resource_type``,
            ``threshold_type``, ``period`` — is immutable; a different shape
            is logically a different trigger and should be created fresh so
            the firings audit table cleanly tracks one configuration over
            time. Every field is Optional; PATCH is partial. An empty body is a
            valid no-op. ``extra='forbid'`` rejects unknown keys with HTTP 422. This catches
            two real customer foot-guns at once: PATCHing an immutable shape
            field (``resource_type`` / ``threshold_type`` / ``period``) used
            to return 200 with the value silently dropped, and a misspelled
            editable field name (e.g. ``threshold_val``) used to return 200
            with no clue the change was ignored. Both now surface as an
            explicit validation error at the boundary.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsageTriggerResponse
    """

    return sync_detailed(
        trigger_id=trigger_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    trigger_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UsageTriggerUpdate,
) -> Response[HTTPValidationError | UsageTriggerResponse]:
    """Update Trigger

     Update a trigger's mutable fields. Three fields are editable: ``is_active`` (deactivate to free a
    slot under the per-tenant cap), ``threshold_value`` (re-tune the trip point as your volume scales),
    and ``event_callback_url`` (change the receiver). The trigger shape — ``resource_type``,
    ``threshold_type``, ``period`` — is immutable; create a new trigger if you need a different shape.
    Returns 404 when the trigger doesn't exist or belongs to another tenant. Returns 400 when
    ``event_callback_url`` is structurally invalid or resolves to a non-public address; 503 when DNS
    resolution is unavailable. An empty body is a valid no-op. Activating (flipping ``is_active`` from
    false to true) re-checks the per-tenant active cap. Re-activating a trigger whose ``resource_type``
    is no longer a supported value returns 422 — create a new trigger with a currently-supported
    ``resource_type`` instead.

    Args:
        trigger_id (UUID):
        body (UsageTriggerUpdate): Partial update for ``PATCH /usage/triggers/{id}``. Only fields
            a customer can re-tune in place are exposed: the
            ``is_active`` flag (deactivate to recover the per-tenant cap
            without losing audit history), the threshold value (re-tune the
            trip point as their volume scales), and the callback URL (rotate
            the receiver). The trigger's *shape* — ``resource_type``,
            ``threshold_type``, ``period`` — is immutable; a different shape
            is logically a different trigger and should be created fresh so
            the firings audit table cleanly tracks one configuration over
            time. Every field is Optional; PATCH is partial. An empty body is a
            valid no-op. ``extra='forbid'`` rejects unknown keys with HTTP 422. This catches
            two real customer foot-guns at once: PATCHing an immutable shape
            field (``resource_type`` / ``threshold_type`` / ``period``) used
            to return 200 with the value silently dropped, and a misspelled
            editable field name (e.g. ``threshold_val``) used to return 200
            with no clue the change was ignored. Both now surface as an
            explicit validation error at the boundary.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsageTriggerResponse]
    """

    kwargs = _get_kwargs(
        trigger_id=trigger_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    trigger_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UsageTriggerUpdate,
) -> HTTPValidationError | UsageTriggerResponse | None:
    """Update Trigger

     Update a trigger's mutable fields. Three fields are editable: ``is_active`` (deactivate to free a
    slot under the per-tenant cap), ``threshold_value`` (re-tune the trip point as your volume scales),
    and ``event_callback_url`` (change the receiver). The trigger shape — ``resource_type``,
    ``threshold_type``, ``period`` — is immutable; create a new trigger if you need a different shape.
    Returns 404 when the trigger doesn't exist or belongs to another tenant. Returns 400 when
    ``event_callback_url`` is structurally invalid or resolves to a non-public address; 503 when DNS
    resolution is unavailable. An empty body is a valid no-op. Activating (flipping ``is_active`` from
    false to true) re-checks the per-tenant active cap. Re-activating a trigger whose ``resource_type``
    is no longer a supported value returns 422 — create a new trigger with a currently-supported
    ``resource_type`` instead.

    Args:
        trigger_id (UUID):
        body (UsageTriggerUpdate): Partial update for ``PATCH /usage/triggers/{id}``. Only fields
            a customer can re-tune in place are exposed: the
            ``is_active`` flag (deactivate to recover the per-tenant cap
            without losing audit history), the threshold value (re-tune the
            trip point as their volume scales), and the callback URL (rotate
            the receiver). The trigger's *shape* — ``resource_type``,
            ``threshold_type``, ``period`` — is immutable; a different shape
            is logically a different trigger and should be created fresh so
            the firings audit table cleanly tracks one configuration over
            time. Every field is Optional; PATCH is partial. An empty body is a
            valid no-op. ``extra='forbid'`` rejects unknown keys with HTTP 422. This catches
            two real customer foot-guns at once: PATCHing an immutable shape
            field (``resource_type`` / ``threshold_type`` / ``period``) used
            to return 200 with the value silently dropped, and a misspelled
            editable field name (e.g. ``threshold_val``) used to return 200
            with no clue the change was ignored. Both now surface as an
            explicit validation error at the boundary.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsageTriggerResponse
    """

    return (
        await asyncio_detailed(
            trigger_id=trigger_id,
            client=client,
            body=body,
        )
    ).parsed
