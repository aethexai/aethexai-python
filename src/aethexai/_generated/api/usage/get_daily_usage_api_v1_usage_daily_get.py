from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.usage_daily_entry import UsageDailyEntry
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID


def _get_kwargs(
    *,
    days: int | Unset = 30,
    api_key_id: None | Unset | UUID = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["days"] = days

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
        "url": "/api/v1/usage/daily",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[UsageDailyEntry] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UsageDailyEntry.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[UsageDailyEntry]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,
    api_key_id: None | Unset | UUID = UNSET,
) -> Response[HTTPValidationError | list[UsageDailyEntry]]:
    """Get Daily Usage

     Per-day usage rollup for the trailing N calendar days.

    ``days`` is a **date window**, not a row limit: the response always
    contains exactly ``days`` entries, one per calendar day in UTC,
    newest-first. Days with no activity are returned as zero-filled
    rows so the response is chart-ready without client-side gap
    handling.

    The 1..365 bound is enforced by Pydantic; values outside that
    range 422 at the boundary.

    Args:
        days (int | Unset):  Default: 30.
        api_key_id (None | Unset | UUID): Restrict the aggregate to usage rows logged against this
            API key. Always tenant-scoped: a key id that belongs to a different tenant (or doesn't
            exist) returns zeros rather than leaking existence.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[UsageDailyEntry]]
    """

    kwargs = _get_kwargs(
        days=days,
        api_key_id=api_key_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,
    api_key_id: None | Unset | UUID = UNSET,
) -> HTTPValidationError | list[UsageDailyEntry] | None:
    """Get Daily Usage

     Per-day usage rollup for the trailing N calendar days.

    ``days`` is a **date window**, not a row limit: the response always
    contains exactly ``days`` entries, one per calendar day in UTC,
    newest-first. Days with no activity are returned as zero-filled
    rows so the response is chart-ready without client-side gap
    handling.

    The 1..365 bound is enforced by Pydantic; values outside that
    range 422 at the boundary.

    Args:
        days (int | Unset):  Default: 30.
        api_key_id (None | Unset | UUID): Restrict the aggregate to usage rows logged against this
            API key. Always tenant-scoped: a key id that belongs to a different tenant (or doesn't
            exist) returns zeros rather than leaking existence.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[UsageDailyEntry]
    """

    return sync_detailed(
        client=client,
        days=days,
        api_key_id=api_key_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,
    api_key_id: None | Unset | UUID = UNSET,
) -> Response[HTTPValidationError | list[UsageDailyEntry]]:
    """Get Daily Usage

     Per-day usage rollup for the trailing N calendar days.

    ``days`` is a **date window**, not a row limit: the response always
    contains exactly ``days`` entries, one per calendar day in UTC,
    newest-first. Days with no activity are returned as zero-filled
    rows so the response is chart-ready without client-side gap
    handling.

    The 1..365 bound is enforced by Pydantic; values outside that
    range 422 at the boundary.

    Args:
        days (int | Unset):  Default: 30.
        api_key_id (None | Unset | UUID): Restrict the aggregate to usage rows logged against this
            API key. Always tenant-scoped: a key id that belongs to a different tenant (or doesn't
            exist) returns zeros rather than leaking existence.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[UsageDailyEntry]]
    """

    kwargs = _get_kwargs(
        days=days,
        api_key_id=api_key_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,
    api_key_id: None | Unset | UUID = UNSET,
) -> HTTPValidationError | list[UsageDailyEntry] | None:
    """Get Daily Usage

     Per-day usage rollup for the trailing N calendar days.

    ``days`` is a **date window**, not a row limit: the response always
    contains exactly ``days`` entries, one per calendar day in UTC,
    newest-first. Days with no activity are returned as zero-filled
    rows so the response is chart-ready without client-side gap
    handling.

    The 1..365 bound is enforced by Pydantic; values outside that
    range 422 at the boundary.

    Args:
        days (int | Unset):  Default: 30.
        api_key_id (None | Unset | UUID): Restrict the aggregate to usage rows logged against this
            API key. Always tenant-scoped: a key id that belongs to a different tenant (or doesn't
            exist) returns zeros rather than leaking existence.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[UsageDailyEntry]
    """

    return (
        await asyncio_detailed(
            client=client,
            days=days,
            api_key_id=api_key_id,
        )
    ).parsed
