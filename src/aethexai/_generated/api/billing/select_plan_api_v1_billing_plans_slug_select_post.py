from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.select_plan_request import SelectPlanRequest
from ...models.select_plan_response import SelectPlanResponse
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    slug: str,
    *,
    body: None | SelectPlanRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/billing/plans/{slug}/select".format(
            slug=quote(str(slug), safe=""),
        ),
    }

    if isinstance(body, SelectPlanRequest):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | SelectPlanResponse | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = SelectPlanResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | SelectPlanResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    slug: str,
    *,
    client: AuthenticatedClient | Client,
    body: None | SelectPlanRequest | Unset = UNSET,
) -> Response[HTTPValidationError | SelectPlanResponse]:
    """Select Plan

     Switch the tenant's subscription to the named plan tier. First-time selection of a paid tier creates
    a new Stripe
    Subscription against the tenant's saved payment method. Subsequent
    selections update the existing Subscription's price item with
    pro-ration. Selecting the free tier cancels the active
    Subscription (the renewal job continues granting free-tier
    credits). Required state:
     * Tenant must have ``has_payment_method=True`` (i.e. attached a
     chargeable card or Link PM via the SetupIntent flow) before
     selecting any paid tier. Free tier is always selectable. * Plan row must have ``stripe_price_id``
    populated (ops sets
     this after creating the Stripe Price). If not populated for
     the requested tier, the route returns 503.

    Args:
        slug (str):
        body (None | SelectPlanRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SelectPlanResponse]
    """

    kwargs = _get_kwargs(
        slug=slug,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    slug: str,
    *,
    client: AuthenticatedClient | Client,
    body: None | SelectPlanRequest | Unset = UNSET,
) -> HTTPValidationError | SelectPlanResponse | None:
    """Select Plan

     Switch the tenant's subscription to the named plan tier. First-time selection of a paid tier creates
    a new Stripe
    Subscription against the tenant's saved payment method. Subsequent
    selections update the existing Subscription's price item with
    pro-ration. Selecting the free tier cancels the active
    Subscription (the renewal job continues granting free-tier
    credits). Required state:
     * Tenant must have ``has_payment_method=True`` (i.e. attached a
     chargeable card or Link PM via the SetupIntent flow) before
     selecting any paid tier. Free tier is always selectable. * Plan row must have ``stripe_price_id``
    populated (ops sets
     this after creating the Stripe Price). If not populated for
     the requested tier, the route returns 503.

    Args:
        slug (str):
        body (None | SelectPlanRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SelectPlanResponse
    """

    return sync_detailed(
        slug=slug,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient | Client,
    body: None | SelectPlanRequest | Unset = UNSET,
) -> Response[HTTPValidationError | SelectPlanResponse]:
    """Select Plan

     Switch the tenant's subscription to the named plan tier. First-time selection of a paid tier creates
    a new Stripe
    Subscription against the tenant's saved payment method. Subsequent
    selections update the existing Subscription's price item with
    pro-ration. Selecting the free tier cancels the active
    Subscription (the renewal job continues granting free-tier
    credits). Required state:
     * Tenant must have ``has_payment_method=True`` (i.e. attached a
     chargeable card or Link PM via the SetupIntent flow) before
     selecting any paid tier. Free tier is always selectable. * Plan row must have ``stripe_price_id``
    populated (ops sets
     this after creating the Stripe Price). If not populated for
     the requested tier, the route returns 503.

    Args:
        slug (str):
        body (None | SelectPlanRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SelectPlanResponse]
    """

    kwargs = _get_kwargs(
        slug=slug,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    *,
    client: AuthenticatedClient | Client,
    body: None | SelectPlanRequest | Unset = UNSET,
) -> HTTPValidationError | SelectPlanResponse | None:
    """Select Plan

     Switch the tenant's subscription to the named plan tier. First-time selection of a paid tier creates
    a new Stripe
    Subscription against the tenant's saved payment method. Subsequent
    selections update the existing Subscription's price item with
    pro-ration. Selecting the free tier cancels the active
    Subscription (the renewal job continues granting free-tier
    credits). Required state:
     * Tenant must have ``has_payment_method=True`` (i.e. attached a
     chargeable card or Link PM via the SetupIntent flow) before
     selecting any paid tier. Free tier is always selectable. * Plan row must have ``stripe_price_id``
    populated (ops sets
     this after creating the Stripe Price). If not populated for
     the requested tier, the route returns 503.

    Args:
        slug (str):
        body (None | SelectPlanRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SelectPlanResponse
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
            body=body,
        )
    ).parsed
