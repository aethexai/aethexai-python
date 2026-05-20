from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.twilio_register_request import TwilioRegisterRequest
from typing import cast


def _get_kwargs(
    *,
    body: TwilioRegisterRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/phone-numbers/twilio/register",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    *,
    client: AuthenticatedClient,
    body: TwilioRegisterRequest,
) -> Response[Any | HTTPValidationError]:
    """Register Twilio

     Register a Twilio phone number under a tenant-owned Twilio account.

    The caller must supply a ``twilio_account_id`` that resolves to an
    active row in ``vo_twilio_accounts`` owned by this tenant -- the
    legacy cluster-wide ``TWILIO_ACCOUNT_SID`` env-var fallback is gone
    (migration 061 wiped any remaining legacy rows). The service uses
    that tenant's credentials to bind the number's Voice URL on
    Twilio's side and persists ``phone_number.twilio_account_id`` so
    update/release can find the same credentials later.

    Status codes:
      * 404 -- agent_id (when supplied) does not exist for this tenant.
      * 422 -- twilio_account_id is invalid / cross-tenant / released,
        or the phone number isn't in the supplied Twilio account.
      * 503 -- encryption key not configured (cannot decrypt the
        Twilio auth_token), or Twilio API unreachable / timed out.

    Args:
        body (TwilioRegisterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
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
    body: TwilioRegisterRequest,
) -> Any | HTTPValidationError | None:
    """Register Twilio

     Register a Twilio phone number under a tenant-owned Twilio account.

    The caller must supply a ``twilio_account_id`` that resolves to an
    active row in ``vo_twilio_accounts`` owned by this tenant -- the
    legacy cluster-wide ``TWILIO_ACCOUNT_SID`` env-var fallback is gone
    (migration 061 wiped any remaining legacy rows). The service uses
    that tenant's credentials to bind the number's Voice URL on
    Twilio's side and persists ``phone_number.twilio_account_id`` so
    update/release can find the same credentials later.

    Status codes:
      * 404 -- agent_id (when supplied) does not exist for this tenant.
      * 422 -- twilio_account_id is invalid / cross-tenant / released,
        or the phone number isn't in the supplied Twilio account.
      * 503 -- encryption key not configured (cannot decrypt the
        Twilio auth_token), or Twilio API unreachable / timed out.

    Args:
        body (TwilioRegisterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TwilioRegisterRequest,
) -> Response[Any | HTTPValidationError]:
    """Register Twilio

     Register a Twilio phone number under a tenant-owned Twilio account.

    The caller must supply a ``twilio_account_id`` that resolves to an
    active row in ``vo_twilio_accounts`` owned by this tenant -- the
    legacy cluster-wide ``TWILIO_ACCOUNT_SID`` env-var fallback is gone
    (migration 061 wiped any remaining legacy rows). The service uses
    that tenant's credentials to bind the number's Voice URL on
    Twilio's side and persists ``phone_number.twilio_account_id`` so
    update/release can find the same credentials later.

    Status codes:
      * 404 -- agent_id (when supplied) does not exist for this tenant.
      * 422 -- twilio_account_id is invalid / cross-tenant / released,
        or the phone number isn't in the supplied Twilio account.
      * 503 -- encryption key not configured (cannot decrypt the
        Twilio auth_token), or Twilio API unreachable / timed out.

    Args:
        body (TwilioRegisterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TwilioRegisterRequest,
) -> Any | HTTPValidationError | None:
    """Register Twilio

     Register a Twilio phone number under a tenant-owned Twilio account.

    The caller must supply a ``twilio_account_id`` that resolves to an
    active row in ``vo_twilio_accounts`` owned by this tenant -- the
    legacy cluster-wide ``TWILIO_ACCOUNT_SID`` env-var fallback is gone
    (migration 061 wiped any remaining legacy rows). The service uses
    that tenant's credentials to bind the number's Voice URL on
    Twilio's side and persists ``phone_number.twilio_account_id`` so
    update/release can find the same credentials later.

    Status codes:
      * 404 -- agent_id (when supplied) does not exist for this tenant.
      * 422 -- twilio_account_id is invalid / cross-tenant / released,
        or the phone number isn't in the supplied Twilio account.
      * 503 -- encryption key not configured (cannot decrypt the
        Twilio auth_token), or Twilio API unreachable / timed out.

    Args:
        body (TwilioRegisterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
