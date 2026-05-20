from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.phone_number_response import PhoneNumberResponse
from typing import cast
from uuid import UUID


def _get_kwargs(
    pn_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/phone-numbers/{pn_id}".format(
            pn_id=quote(str(pn_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PhoneNumberResponse | None:
    if response.status_code == 200:
        response_200 = PhoneNumberResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | PhoneNumberResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pn_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | PhoneNumberResponse]:
    """Get Phone Number

    Args:
        pn_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PhoneNumberResponse]
    """

    kwargs = _get_kwargs(
        pn_id=pn_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pn_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | PhoneNumberResponse | None:
    """Get Phone Number

    Args:
        pn_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PhoneNumberResponse
    """

    return sync_detailed(
        pn_id=pn_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    pn_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | PhoneNumberResponse]:
    """Get Phone Number

    Args:
        pn_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PhoneNumberResponse]
    """

    kwargs = _get_kwargs(
        pn_id=pn_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pn_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | PhoneNumberResponse | None:
    """Get Phone Number

    Args:
        pn_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PhoneNumberResponse
    """

    return (
        await asyncio_detailed(
            pn_id=pn_id,
            client=client,
        )
    ).parsed
