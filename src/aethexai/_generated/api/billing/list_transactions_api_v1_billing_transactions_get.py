from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.transaction_list_response import TransactionListResponse
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    cursor: None | str | Unset = UNSET,
    next_cursor: None | str | Unset = UNSET,
    page_size: int | Unset = 25,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    json_next_cursor: None | str | Unset
    if isinstance(next_cursor, Unset):
        json_next_cursor = UNSET
    else:
        json_next_cursor = next_cursor
    params["next_cursor"] = json_next_cursor

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/billing/transactions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TransactionListResponse | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = TransactionListResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | TransactionListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    cursor: None | str | Unset = UNSET,
    next_cursor: None | str | Unset = UNSET,
    page_size: int | Unset = 25,
) -> Response[HTTPValidationError | TransactionListResponse]:
    """List Transactions

     Paginated credit ledger, newest-first.

    Args:
        cursor (None | str | Unset): Opaque cursor from the previous page's ``next_cursor``. Also
            accepted as ``?next_cursor=`` for clients that echo the response field name directly.
        next_cursor (None | str | Unset): Alias for ``cursor``. Accepted so a client reading the
            response field ``next_cursor`` and passing it back as a query param works without
            surprises. Prefer ``cursor``.
        page_size (int | Unset):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TransactionListResponse]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        next_cursor=next_cursor,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    cursor: None | str | Unset = UNSET,
    next_cursor: None | str | Unset = UNSET,
    page_size: int | Unset = 25,
) -> HTTPValidationError | TransactionListResponse | None:
    """List Transactions

     Paginated credit ledger, newest-first.

    Args:
        cursor (None | str | Unset): Opaque cursor from the previous page's ``next_cursor``. Also
            accepted as ``?next_cursor=`` for clients that echo the response field name directly.
        next_cursor (None | str | Unset): Alias for ``cursor``. Accepted so a client reading the
            response field ``next_cursor`` and passing it back as a query param works without
            surprises. Prefer ``cursor``.
        page_size (int | Unset):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TransactionListResponse
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        next_cursor=next_cursor,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    cursor: None | str | Unset = UNSET,
    next_cursor: None | str | Unset = UNSET,
    page_size: int | Unset = 25,
) -> Response[HTTPValidationError | TransactionListResponse]:
    """List Transactions

     Paginated credit ledger, newest-first.

    Args:
        cursor (None | str | Unset): Opaque cursor from the previous page's ``next_cursor``. Also
            accepted as ``?next_cursor=`` for clients that echo the response field name directly.
        next_cursor (None | str | Unset): Alias for ``cursor``. Accepted so a client reading the
            response field ``next_cursor`` and passing it back as a query param works without
            surprises. Prefer ``cursor``.
        page_size (int | Unset):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TransactionListResponse]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        next_cursor=next_cursor,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    cursor: None | str | Unset = UNSET,
    next_cursor: None | str | Unset = UNSET,
    page_size: int | Unset = 25,
) -> HTTPValidationError | TransactionListResponse | None:
    """List Transactions

     Paginated credit ledger, newest-first.

    Args:
        cursor (None | str | Unset): Opaque cursor from the previous page's ``next_cursor``. Also
            accepted as ``?next_cursor=`` for clients that echo the response field name directly.
        next_cursor (None | str | Unset): Alias for ``cursor``. Accepted so a client reading the
            response field ``next_cursor`` and passing it back as a query param works without
            surprises. Prefer ``cursor``.
        page_size (int | Unset):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TransactionListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            next_cursor=next_cursor,
            page_size=page_size,
        )
    ).parsed
