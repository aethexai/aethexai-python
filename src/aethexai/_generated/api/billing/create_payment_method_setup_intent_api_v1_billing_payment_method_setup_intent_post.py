from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.setup_intent_response import SetupIntentResponse
from typing import cast


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/billing/payment-method/setup-intent",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> SetupIntentResponse | None:
    if response.status_code == 201:
        response_201 = SetupIntentResponse.from_dict(response.json())

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[SetupIntentResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[SetupIntentResponse]:
    """Create Payment Method Setup Intent

     Return a SetupIntent the portal Payment Element can confirm
    against to attach a card to the tenant's Stripe Customer. ``usage='off_session'`` is set on the
    SetupIntent so the saved
    card can be charged later for PAYG overage without re-prompting
    for 3DS. Customer is created lazily on first call.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SetupIntentResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> SetupIntentResponse | None:
    """Create Payment Method Setup Intent

     Return a SetupIntent the portal Payment Element can confirm
    against to attach a card to the tenant's Stripe Customer. ``usage='off_session'`` is set on the
    SetupIntent so the saved
    card can be charged later for PAYG overage without re-prompting
    for 3DS. Customer is created lazily on first call.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SetupIntentResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[SetupIntentResponse]:
    """Create Payment Method Setup Intent

     Return a SetupIntent the portal Payment Element can confirm
    against to attach a card to the tenant's Stripe Customer. ``usage='off_session'`` is set on the
    SetupIntent so the saved
    card can be charged later for PAYG overage without re-prompting
    for 3DS. Customer is created lazily on first call.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SetupIntentResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> SetupIntentResponse | None:
    """Create Payment Method Setup Intent

     Return a SetupIntent the portal Payment Element can confirm
    against to attach a card to the tenant's Stripe Customer. ``usage='off_session'`` is set on the
    SetupIntent so the saved
    card can be charged later for PAYG overage without re-prompting
    for 3DS. Customer is created lazily on first call.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SetupIntentResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
