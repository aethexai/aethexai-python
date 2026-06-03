from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response import PaginatedResponse
from ...types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime


def _get_kwargs(
    *,
    offset: int | Unset = 0,
    limit: int | Unset = 50,
    sort: str | Unset = "-created_at",
    name: None | str | Unset = UNSET,
    created_at: datetime.date | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["offset"] = offset

    params["limit"] = limit

    params["sort"] = sort

    json_name: None | str | Unset
    if isinstance(name, Unset):
        json_name = UNSET
    else:
        json_name = name
    params["name"] = json_name

    json_created_at: None | str | Unset
    if isinstance(created_at, Unset):
        json_created_at = UNSET
    elif isinstance(created_at, datetime.date):
        json_created_at = created_at.isoformat()
    else:
        json_created_at = created_at
    params["created_at"] = json_created_at

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/admin/tenants",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PaginatedResponse | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = PaginatedResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | PaginatedResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    offset: int | Unset = 0,
    limit: int | Unset = 50,
    sort: str | Unset = "-created_at",
    name: None | str | Unset = UNSET,
    created_at: datetime.date | None | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponse]:
    """List Admin Tenants

     Paginated table of every tenant with its lifetime request count. ``request_count`` is the tenant's
    all-time request count from the daily
    rollup; tenants with no traffic still appear (count 0). ``sort`` is
    validated against a fixed allowlist; an unknown value falls back to
    newest-first. The page of tenants is selected first, then request counts are read from
    the rollup only for that page's tenant ids — so a single page never scans
    ```` at all. The sort always carries ``Tenant.id`` as a
    tie-breaker so pagination is stable even when the primary key
    (``created_at`` / ``name`` / ``status`` / credits) ties.

    Args:
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        sort (str | Unset):  Default: '-created_at'.
        name (None | str | Unset):
        created_at (datetime.date | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponse]
    """

    kwargs = _get_kwargs(
        offset=offset,
        limit=limit,
        sort=sort,
        name=name,
        created_at=created_at,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    offset: int | Unset = 0,
    limit: int | Unset = 50,
    sort: str | Unset = "-created_at",
    name: None | str | Unset = UNSET,
    created_at: datetime.date | None | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponse | None:
    """List Admin Tenants

     Paginated table of every tenant with its lifetime request count. ``request_count`` is the tenant's
    all-time request count from the daily
    rollup; tenants with no traffic still appear (count 0). ``sort`` is
    validated against a fixed allowlist; an unknown value falls back to
    newest-first. The page of tenants is selected first, then request counts are read from
    the rollup only for that page's tenant ids — so a single page never scans
    ```` at all. The sort always carries ``Tenant.id`` as a
    tie-breaker so pagination is stable even when the primary key
    (``created_at`` / ``name`` / ``status`` / credits) ties.

    Args:
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        sort (str | Unset):  Default: '-created_at'.
        name (None | str | Unset):
        created_at (datetime.date | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponse
    """

    return sync_detailed(
        client=client,
        offset=offset,
        limit=limit,
        sort=sort,
        name=name,
        created_at=created_at,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    offset: int | Unset = 0,
    limit: int | Unset = 50,
    sort: str | Unset = "-created_at",
    name: None | str | Unset = UNSET,
    created_at: datetime.date | None | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponse]:
    """List Admin Tenants

     Paginated table of every tenant with its lifetime request count. ``request_count`` is the tenant's
    all-time request count from the daily
    rollup; tenants with no traffic still appear (count 0). ``sort`` is
    validated against a fixed allowlist; an unknown value falls back to
    newest-first. The page of tenants is selected first, then request counts are read from
    the rollup only for that page's tenant ids — so a single page never scans
    ```` at all. The sort always carries ``Tenant.id`` as a
    tie-breaker so pagination is stable even when the primary key
    (``created_at`` / ``name`` / ``status`` / credits) ties.

    Args:
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        sort (str | Unset):  Default: '-created_at'.
        name (None | str | Unset):
        created_at (datetime.date | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponse]
    """

    kwargs = _get_kwargs(
        offset=offset,
        limit=limit,
        sort=sort,
        name=name,
        created_at=created_at,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    offset: int | Unset = 0,
    limit: int | Unset = 50,
    sort: str | Unset = "-created_at",
    name: None | str | Unset = UNSET,
    created_at: datetime.date | None | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponse | None:
    """List Admin Tenants

     Paginated table of every tenant with its lifetime request count. ``request_count`` is the tenant's
    all-time request count from the daily
    rollup; tenants with no traffic still appear (count 0). ``sort`` is
    validated against a fixed allowlist; an unknown value falls back to
    newest-first. The page of tenants is selected first, then request counts are read from
    the rollup only for that page's tenant ids — so a single page never scans
    ```` at all. The sort always carries ``Tenant.id`` as a
    tie-breaker so pagination is stable even when the primary key
    (``created_at`` / ``name`` / ``status`` / credits) ties.

    Args:
        offset (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        sort (str | Unset):  Default: '-created_at'.
        name (None | str | Unset):
        created_at (datetime.date | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            offset=offset,
            limit=limit,
            sort=sort,
            name=name,
            created_at=created_at,
        )
    ).parsed
