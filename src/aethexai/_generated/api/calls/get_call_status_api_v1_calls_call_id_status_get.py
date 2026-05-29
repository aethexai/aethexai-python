from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.call_status_response import CallStatusResponse
from ...models.http_validation_error import HTTPValidationError
from typing import cast
from uuid import UUID


def _get_kwargs(
    call_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/calls/{call_id}/status".format(
            call_id=quote(str(call_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CallStatusResponse | HTTPValidationError | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = CallStatusResponse.from_dict(response.json())

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
) -> Response[CallStatusResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    call_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CallStatusResponse | HTTPValidationError]:
    """Get Call Status

     Return telephony status for a call. Today's writers emit one of the eight values enumerated by
    ``CallStatusLiteral`` (queued / ringing / in-progress / completed /
    failed / no-answer / busy / canceled). ``connected`` is intentionally
    absent: no code path writes it today, and including it would imply an
    observable state customers cannot reach. See. ``CallStatusResponse.status`` is typed as ``str``
    rather than
    ``CallStatusLiteral`` to remain forward-compatible with historical
    ```` rows whose status (e.g. ``'initiated'``, still referenced
    in ``post_call.py``'s CASE expression) sits outside that closed set. The route's *filter* boundary
    (``GET /calls?status=...``) is the strict
    one — it rejects junk inputs at 422 — and the response is the lenient
    one so legacy data round-trips cleanly.

    Args:
        call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallStatusResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        call_id=call_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    call_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CallStatusResponse | HTTPValidationError | None:
    """Get Call Status

     Return telephony status for a call. Today's writers emit one of the eight values enumerated by
    ``CallStatusLiteral`` (queued / ringing / in-progress / completed /
    failed / no-answer / busy / canceled). ``connected`` is intentionally
    absent: no code path writes it today, and including it would imply an
    observable state customers cannot reach. See. ``CallStatusResponse.status`` is typed as ``str``
    rather than
    ``CallStatusLiteral`` to remain forward-compatible with historical
    ```` rows whose status (e.g. ``'initiated'``, still referenced
    in ``post_call.py``'s CASE expression) sits outside that closed set. The route's *filter* boundary
    (``GET /calls?status=...``) is the strict
    one — it rejects junk inputs at 422 — and the response is the lenient
    one so legacy data round-trips cleanly.

    Args:
        call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallStatusResponse | HTTPValidationError
    """

    return sync_detailed(
        call_id=call_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    call_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CallStatusResponse | HTTPValidationError]:
    """Get Call Status

     Return telephony status for a call. Today's writers emit one of the eight values enumerated by
    ``CallStatusLiteral`` (queued / ringing / in-progress / completed /
    failed / no-answer / busy / canceled). ``connected`` is intentionally
    absent: no code path writes it today, and including it would imply an
    observable state customers cannot reach. See. ``CallStatusResponse.status`` is typed as ``str``
    rather than
    ``CallStatusLiteral`` to remain forward-compatible with historical
    ```` rows whose status (e.g. ``'initiated'``, still referenced
    in ``post_call.py``'s CASE expression) sits outside that closed set. The route's *filter* boundary
    (``GET /calls?status=...``) is the strict
    one — it rejects junk inputs at 422 — and the response is the lenient
    one so legacy data round-trips cleanly.

    Args:
        call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallStatusResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        call_id=call_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    call_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CallStatusResponse | HTTPValidationError | None:
    """Get Call Status

     Return telephony status for a call. Today's writers emit one of the eight values enumerated by
    ``CallStatusLiteral`` (queued / ringing / in-progress / completed /
    failed / no-answer / busy / canceled). ``connected`` is intentionally
    absent: no code path writes it today, and including it would imply an
    observable state customers cannot reach. See. ``CallStatusResponse.status`` is typed as ``str``
    rather than
    ``CallStatusLiteral`` to remain forward-compatible with historical
    ```` rows whose status (e.g. ``'initiated'``, still referenced
    in ``post_call.py``'s CASE expression) sits outside that closed set. The route's *filter* boundary
    (``GET /calls?status=...``) is the strict
    one — it rejects junk inputs at 422 — and the response is the lenient
    one so legacy data round-trips cleanly.

    Args:
        call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallStatusResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            call_id=call_id,
            client=client,
        )
    ).parsed
