from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.twilio_account_create import TwilioAccountCreate
from ...models.twilio_account_response import TwilioAccountResponse
from typing import cast


def _get_kwargs(
    *,
    body: TwilioAccountCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/twilio-accounts",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TwilioAccountResponse | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_201 = TwilioAccountResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | TwilioAccountResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TwilioAccountCreate,
) -> Response[HTTPValidationError | TwilioAccountResponse]:
    """Register Twilio Account

     Register a Twilio Account SID for this tenant. The supplied ``account_sid`` + ``auth_token`` pair is validated against Twilio; the SID and an encrypted copy of the auth token are stored (the token is used for inbound-webhook signature verification and outbound calls). Status codes: ``422`` - Twilio rejected the credentials, or the fetched SID does not match the supplied SID; ``409`` - the Account SID is already registered, or the tenant has reached its active-account limit; ``429`` - registration rate limit exceeded; ``503`` - the Twilio API was unavailable or timed out.

    Args:
        body (TwilioAccountCreate): Request body for ``POST /api/v1/twilio-accounts``.
            ``auth_token`` is required at registration time so we can verify the
            SID/token pair with Twilio before persisting.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TwilioAccountResponse]
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
    body: TwilioAccountCreate,
) -> HTTPValidationError | TwilioAccountResponse | None:
    """Register Twilio Account

     Register a Twilio Account SID for this tenant. The supplied ``account_sid`` + ``auth_token`` pair is validated against Twilio; the SID and an encrypted copy of the auth token are stored (the token is used for inbound-webhook signature verification and outbound calls). Status codes: ``422`` - Twilio rejected the credentials, or the fetched SID does not match the supplied SID; ``409`` - the Account SID is already registered, or the tenant has reached its active-account limit; ``429`` - registration rate limit exceeded; ``503`` - the Twilio API was unavailable or timed out.

    Args:
        body (TwilioAccountCreate): Request body for ``POST /api/v1/twilio-accounts``.
            ``auth_token`` is required at registration time so we can verify the
            SID/token pair with Twilio before persisting.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TwilioAccountResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TwilioAccountCreate,
) -> Response[HTTPValidationError | TwilioAccountResponse]:
    """Register Twilio Account

     Register a Twilio Account SID for this tenant. The supplied ``account_sid`` + ``auth_token`` pair is validated against Twilio; the SID and an encrypted copy of the auth token are stored (the token is used for inbound-webhook signature verification and outbound calls). Status codes: ``422`` - Twilio rejected the credentials, or the fetched SID does not match the supplied SID; ``409`` - the Account SID is already registered, or the tenant has reached its active-account limit; ``429`` - registration rate limit exceeded; ``503`` - the Twilio API was unavailable or timed out.

    Args:
        body (TwilioAccountCreate): Request body for ``POST /api/v1/twilio-accounts``.
            ``auth_token`` is required at registration time so we can verify the
            SID/token pair with Twilio before persisting.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TwilioAccountResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TwilioAccountCreate,
) -> HTTPValidationError | TwilioAccountResponse | None:
    """Register Twilio Account

     Register a Twilio Account SID for this tenant. The supplied ``account_sid`` + ``auth_token`` pair is validated against Twilio; the SID and an encrypted copy of the auth token are stored (the token is used for inbound-webhook signature verification and outbound calls). Status codes: ``422`` - Twilio rejected the credentials, or the fetched SID does not match the supplied SID; ``409`` - the Account SID is already registered, or the tenant has reached its active-account limit; ``429`` - registration rate limit exceeded; ``503`` - the Twilio API was unavailable or timed out.

    Args:
        body (TwilioAccountCreate): Request body for ``POST /api/v1/twilio-accounts``.
            ``auth_token`` is required at registration time so we can verify the
            SID/token pair with Twilio before persisting.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TwilioAccountResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
