from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.usage_trigger_create import UsageTriggerCreate
from ...models.usage_trigger_response import UsageTriggerResponse
from typing import cast


def _get_kwargs(
    *,
    body: UsageTriggerCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/usage/triggers",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | UsageTriggerResponse | None:
    if response.status_code == 201:
        response_201 = UsageTriggerResponse.from_dict(response.json())

        return response_201

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
    *,
    client: AuthenticatedClient,
    body: UsageTriggerCreate,
) -> Response[HTTPValidationError | UsageTriggerResponse]:
    """Create Trigger

     Configure a usage threshold + callback URL. The evaluator (ARQ cron, every 5 minutes) checks active
    triggers
    and posts a signed webhook when the threshold is crossed for the
    period. One firing per period; the trigger auto-rearms when the
    period rolls over. Returns 409 when the tenant already has the per-tenant cap of
    active triggers; PATCH ``is_active=false`` on an existing trigger
    to recover a slot before adding a new one. Returns 400 when the tenant has no ``webhook_secret``
    configured. Triggers without a signing secret would deliver an unsigned
    webhook (or, more precisely, would be skipped by the evaluator
    and audited as ``failed`` with no ability to deliver), so we
    refuse the create at the boundary instead of accepting a
    configuration that will never fire. The customer's recovery is
    a single ``POST /usage/webhook-secret/rotate``.

    Args:
        body (UsageTriggerCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsageTriggerResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: UsageTriggerCreate,
) -> HTTPValidationError | UsageTriggerResponse | None:
    """Create Trigger

     Configure a usage threshold + callback URL. The evaluator (ARQ cron, every 5 minutes) checks active
    triggers
    and posts a signed webhook when the threshold is crossed for the
    period. One firing per period; the trigger auto-rearms when the
    period rolls over. Returns 409 when the tenant already has the per-tenant cap of
    active triggers; PATCH ``is_active=false`` on an existing trigger
    to recover a slot before adding a new one. Returns 400 when the tenant has no ``webhook_secret``
    configured. Triggers without a signing secret would deliver an unsigned
    webhook (or, more precisely, would be skipped by the evaluator
    and audited as ``failed`` with no ability to deliver), so we
    refuse the create at the boundary instead of accepting a
    configuration that will never fire. The customer's recovery is
    a single ``POST /usage/webhook-secret/rotate``.

    Args:
        body (UsageTriggerCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsageTriggerResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: UsageTriggerCreate,
) -> Response[HTTPValidationError | UsageTriggerResponse]:
    """Create Trigger

     Configure a usage threshold + callback URL. The evaluator (ARQ cron, every 5 minutes) checks active
    triggers
    and posts a signed webhook when the threshold is crossed for the
    period. One firing per period; the trigger auto-rearms when the
    period rolls over. Returns 409 when the tenant already has the per-tenant cap of
    active triggers; PATCH ``is_active=false`` on an existing trigger
    to recover a slot before adding a new one. Returns 400 when the tenant has no ``webhook_secret``
    configured. Triggers without a signing secret would deliver an unsigned
    webhook (or, more precisely, would be skipped by the evaluator
    and audited as ``failed`` with no ability to deliver), so we
    refuse the create at the boundary instead of accepting a
    configuration that will never fire. The customer's recovery is
    a single ``POST /usage/webhook-secret/rotate``.

    Args:
        body (UsageTriggerCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsageTriggerResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: UsageTriggerCreate,
) -> HTTPValidationError | UsageTriggerResponse | None:
    """Create Trigger

     Configure a usage threshold + callback URL. The evaluator (ARQ cron, every 5 minutes) checks active
    triggers
    and posts a signed webhook when the threshold is crossed for the
    period. One firing per period; the trigger auto-rearms when the
    period rolls over. Returns 409 when the tenant already has the per-tenant cap of
    active triggers; PATCH ``is_active=false`` on an existing trigger
    to recover a slot before adding a new one. Returns 400 when the tenant has no ``webhook_secret``
    configured. Triggers without a signing secret would deliver an unsigned
    webhook (or, more precisely, would be skipped by the evaluator
    and audited as ``failed`` with no ability to deliver), so we
    refuse the create at the boundary instead of accepting a
    configuration that will never fire. The customer's recovery is
    a single ``POST /usage/webhook-secret/rotate``.

    Args:
        body (UsageTriggerCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsageTriggerResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
