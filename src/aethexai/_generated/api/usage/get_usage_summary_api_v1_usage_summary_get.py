from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.usage_summary import UsageSummary
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID


def _get_kwargs(
    *,
    api_key_id: None | Unset | UUID = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_api_key_id: None | str | Unset
    if isinstance(api_key_id, Unset):
        json_api_key_id = UNSET
    elif isinstance(api_key_id, UUID):
        json_api_key_id = str(api_key_id)
    else:
        json_api_key_id = api_key_id
    params["api_key_id"] = json_api_key_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/usage/summary",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | UsageSummary | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = UsageSummary.from_dict(response.json())

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
) -> Response[HTTPValidationError | UsageSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    api_key_id: None | Unset | UUID = UNSET,
) -> Response[HTTPValidationError | UsageSummary]:
    """Get Usage Summary

     Alias for GET /usage.

    Args:
        api_key_id (None | Unset | UUID): Restrict the aggregate to usage rows logged against this
            API key. Always tenant-scoped: a key id that belongs to a different tenant (or doesn't
            exist) returns zeros rather than leaking existence.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsageSummary]
    """

    kwargs = _get_kwargs(
        api_key_id=api_key_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    api_key_id: None | Unset | UUID = UNSET,
) -> HTTPValidationError | UsageSummary | None:
    """Get Usage Summary

     Alias for GET /usage.

    Args:
        api_key_id (None | Unset | UUID): Restrict the aggregate to usage rows logged against this
            API key. Always tenant-scoped: a key id that belongs to a different tenant (or doesn't
            exist) returns zeros rather than leaking existence.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsageSummary
    """

    return sync_detailed(
        client=client,
        api_key_id=api_key_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    api_key_id: None | Unset | UUID = UNSET,
) -> Response[HTTPValidationError | UsageSummary]:
    """Get Usage Summary

     Alias for GET /usage.

    Args:
        api_key_id (None | Unset | UUID): Restrict the aggregate to usage rows logged against this
            API key. Always tenant-scoped: a key id that belongs to a different tenant (or doesn't
            exist) returns zeros rather than leaking existence.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsageSummary]
    """

    kwargs = _get_kwargs(
        api_key_id=api_key_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    api_key_id: None | Unset | UUID = UNSET,
) -> HTTPValidationError | UsageSummary | None:
    """Get Usage Summary

     Alias for GET /usage.

    Args:
        api_key_id (None | Unset | UUID): Restrict the aggregate to usage rows logged against this
            API key. Always tenant-scoped: a key id that belongs to a different tenant (or doesn't
            exist) returns zeros rather than leaking existence.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsageSummary
    """

    return (
        await asyncio_detailed(
            client=client,
            api_key_id=api_key_id,
        )
    ).parsed
