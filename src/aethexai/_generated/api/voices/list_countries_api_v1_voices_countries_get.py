from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_countries_api_v1_voices_countries_get_response_200_item import (
    ListCountriesApiV1VoicesCountriesGetResponse200Item,
)
from typing import cast


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/voices/countries",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[ListCountriesApiV1VoicesCountriesGetResponse200Item] | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListCountriesApiV1VoicesCountriesGetResponse200Item.from_dict(
                response_200_item_data
            )

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[ListCountriesApiV1VoicesCountriesGetResponse200Item]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[list[ListCountriesApiV1VoicesCountriesGetResponse200Item]]:
    r"""List Countries

     Return the closed set of ISO 3166-1 alpha-2 country codes accepted
    by the ``?country=`` filter on ``GET /voices`` and by the curator
    PATCH on ``country``. Wire shape is a list of ``{\"code\": \"NG\", \"name\": \"Nigeria\"}`` objects
    sorted by code so SDKs and the developer-portal country picker can
    render the catalogue without hardcoding the list. Gated behind
    ``voices:read`` so the surface matches the rest of ``/voices/*``;
    the data is static configuration but the endpoint sits on the public
    API and every other voices listing already requires the same scope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ListCountriesApiV1VoicesCountriesGetResponse200Item]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> list[ListCountriesApiV1VoicesCountriesGetResponse200Item] | None:
    r"""List Countries

     Return the closed set of ISO 3166-1 alpha-2 country codes accepted
    by the ``?country=`` filter on ``GET /voices`` and by the curator
    PATCH on ``country``. Wire shape is a list of ``{\"code\": \"NG\", \"name\": \"Nigeria\"}`` objects
    sorted by code so SDKs and the developer-portal country picker can
    render the catalogue without hardcoding the list. Gated behind
    ``voices:read`` so the surface matches the rest of ``/voices/*``;
    the data is static configuration but the endpoint sits on the public
    API and every other voices listing already requires the same scope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ListCountriesApiV1VoicesCountriesGetResponse200Item]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[list[ListCountriesApiV1VoicesCountriesGetResponse200Item]]:
    r"""List Countries

     Return the closed set of ISO 3166-1 alpha-2 country codes accepted
    by the ``?country=`` filter on ``GET /voices`` and by the curator
    PATCH on ``country``. Wire shape is a list of ``{\"code\": \"NG\", \"name\": \"Nigeria\"}`` objects
    sorted by code so SDKs and the developer-portal country picker can
    render the catalogue without hardcoding the list. Gated behind
    ``voices:read`` so the surface matches the rest of ``/voices/*``;
    the data is static configuration but the endpoint sits on the public
    API and every other voices listing already requires the same scope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ListCountriesApiV1VoicesCountriesGetResponse200Item]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> list[ListCountriesApiV1VoicesCountriesGetResponse200Item] | None:
    r"""List Countries

     Return the closed set of ISO 3166-1 alpha-2 country codes accepted
    by the ``?country=`` filter on ``GET /voices`` and by the curator
    PATCH on ``country``. Wire shape is a list of ``{\"code\": \"NG\", \"name\": \"Nigeria\"}`` objects
    sorted by code so SDKs and the developer-portal country picker can
    render the catalogue without hardcoding the list. Gated behind
    ``voices:read`` so the surface matches the rest of ``/voices/*``;
    the data is static configuration but the endpoint sits on the public
    API and every other voices listing already requires the same scope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ListCountriesApiV1VoicesCountriesGetResponse200Item]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
