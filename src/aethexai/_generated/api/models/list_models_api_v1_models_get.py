from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.model_entry import ModelEntry
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    include_unavailable: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["include_unavailable"] = include_unavailable

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/models",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[ModelEntry] | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ModelEntry.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[ModelEntry]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    include_unavailable: bool | Unset = False,
) -> Response[HTTPValidationError | list[ModelEntry]]:
    """List Models

     Return the available LLM model catalog for this deployment. Each entry includes an ``available``
    flag. By default only currently-usable models are returned; pass ``?include_unavailable=true`` to
    also list models that are not currently usable (returned with ``available: false``). Models not in
    the catalog are rejected with a 422 on agent create/update.

    Args:
        include_unavailable (bool | Unset): Include models whose upstream provider key is not
            configured on this deployment. Default false so SDK model pickers only see names that will
            actually route externally. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ModelEntry]]
    """

    kwargs = _get_kwargs(
        include_unavailable=include_unavailable,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    include_unavailable: bool | Unset = False,
) -> HTTPValidationError | list[ModelEntry] | None:
    """List Models

     Return the available LLM model catalog for this deployment. Each entry includes an ``available``
    flag. By default only currently-usable models are returned; pass ``?include_unavailable=true`` to
    also list models that are not currently usable (returned with ``available: false``). Models not in
    the catalog are rejected with a 422 on agent create/update.

    Args:
        include_unavailable (bool | Unset): Include models whose upstream provider key is not
            configured on this deployment. Default false so SDK model pickers only see names that will
            actually route externally. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ModelEntry]
    """

    return sync_detailed(
        client=client,
        include_unavailable=include_unavailable,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    include_unavailable: bool | Unset = False,
) -> Response[HTTPValidationError | list[ModelEntry]]:
    """List Models

     Return the available LLM model catalog for this deployment. Each entry includes an ``available``
    flag. By default only currently-usable models are returned; pass ``?include_unavailable=true`` to
    also list models that are not currently usable (returned with ``available: false``). Models not in
    the catalog are rejected with a 422 on agent create/update.

    Args:
        include_unavailable (bool | Unset): Include models whose upstream provider key is not
            configured on this deployment. Default false so SDK model pickers only see names that will
            actually route externally. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ModelEntry]]
    """

    kwargs = _get_kwargs(
        include_unavailable=include_unavailable,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    include_unavailable: bool | Unset = False,
) -> HTTPValidationError | list[ModelEntry] | None:
    """List Models

     Return the available LLM model catalog for this deployment. Each entry includes an ``available``
    flag. By default only currently-usable models are returned; pass ``?include_unavailable=true`` to
    also list models that are not currently usable (returned with ``available: false``). Models not in
    the catalog are rejected with a 422 on agent create/update.

    Args:
        include_unavailable (bool | Unset): Include models whose upstream provider key is not
            configured on this deployment. Default false so SDK model pickers only see names that will
            actually route externally. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ModelEntry]
    """

    return (
        await asyncio_detailed(
            client=client,
            include_unavailable=include_unavailable,
        )
    ).parsed
