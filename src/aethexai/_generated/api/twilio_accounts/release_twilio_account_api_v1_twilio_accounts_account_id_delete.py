from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import cast
from uuid import UUID


def _get_kwargs(
    account_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/v1/twilio-accounts/{account_id}".format(
            account_id=quote(str(account_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_204 = cast(Any, None)
        return response_204

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
    account_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Any | HTTPValidationError]:
    """Release Twilio Account

     Mark the row released so the active Account SID slot frees up. Idempotent: returns 204 whether the
    row was active, already released,
    or never existed under this tenant. The DB ``get`` already enforces
    tenant scope (``WHERE tenant_id =:tenant``) so the swallowed
    ``NotFoundError`` cannot leak cross-tenant rows -- a request from
    tenant A targeting tenant B's row gets the same 204 as if the row
    didn't exist, which is the desired idempotent shape. Status codes:
     * 204 -- row released, already released, or not found under tenant. * 503 -- server-side encryption
    key missing/malformed while
     scrubbing the stored credential.

    Args:
        account_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Any | HTTPValidationError | None:
    """Release Twilio Account

     Mark the row released so the active Account SID slot frees up. Idempotent: returns 204 whether the
    row was active, already released,
    or never existed under this tenant. The DB ``get`` already enforces
    tenant scope (``WHERE tenant_id =:tenant``) so the swallowed
    ``NotFoundError`` cannot leak cross-tenant rows -- a request from
    tenant A targeting tenant B's row gets the same 204 as if the row
    didn't exist, which is the desired idempotent shape. Status codes:
     * 204 -- row released, already released, or not found under tenant. * 503 -- server-side encryption
    key missing/malformed while
     scrubbing the stored credential.

    Args:
        account_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    account_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Any | HTTPValidationError]:
    """Release Twilio Account

     Mark the row released so the active Account SID slot frees up. Idempotent: returns 204 whether the
    row was active, already released,
    or never existed under this tenant. The DB ``get`` already enforces
    tenant scope (``WHERE tenant_id =:tenant``) so the swallowed
    ``NotFoundError`` cannot leak cross-tenant rows -- a request from
    tenant A targeting tenant B's row gets the same 204 as if the row
    didn't exist, which is the desired idempotent shape. Status codes:
     * 204 -- row released, already released, or not found under tenant. * 503 -- server-side encryption
    key missing/malformed while
     scrubbing the stored credential.

    Args:
        account_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Any | HTTPValidationError | None:
    """Release Twilio Account

     Mark the row released so the active Account SID slot frees up. Idempotent: returns 204 whether the
    row was active, already released,
    or never existed under this tenant. The DB ``get`` already enforces
    tenant scope (``WHERE tenant_id =:tenant``) so the swallowed
    ``NotFoundError`` cannot leak cross-tenant rows -- a request from
    tenant A targeting tenant B's row gets the same 204 as if the row
    didn't exist, which is the desired idempotent shape. Status codes:
     * 204 -- row released, already released, or not found under tenant. * 503 -- server-side encryption
    key missing/malformed while
     scrubbing the stored credential.

    Args:
        account_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
        )
    ).parsed
