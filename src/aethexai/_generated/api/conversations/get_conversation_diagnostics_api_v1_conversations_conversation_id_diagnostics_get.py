from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.conversation_diagnostics_response import ConversationDiagnosticsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID


def _get_kwargs(
    conversation_id: UUID,
    *,
    limit: int | Unset = 500,
    event_type: None | str | Unset = UNSET,
    stage: None | str | Unset = UNSET,
    severity: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    json_event_type: None | str | Unset
    if isinstance(event_type, Unset):
        json_event_type = UNSET
    else:
        json_event_type = event_type
    params["event_type"] = json_event_type

    json_stage: None | str | Unset
    if isinstance(stage, Unset):
        json_stage = UNSET
    else:
        json_stage = stage
    params["stage"] = json_stage

    json_severity: None | str | Unset
    if isinstance(severity, Unset):
        json_severity = UNSET
    else:
        json_severity = severity
    params["severity"] = json_severity

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/conversations/{conversation_id}/diagnostics".format(
            conversation_id=quote(str(conversation_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ConversationDiagnosticsResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = ConversationDiagnosticsResponse.from_dict(response.json())

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
) -> Response[ConversationDiagnosticsResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    conversation_id: UUID,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 500,
    event_type: None | str | Unset = UNSET,
    stage: None | str | Unset = UNSET,
    severity: None | str | Unset = UNSET,
) -> Response[ConversationDiagnosticsResponse | HTTPValidationError]:
    """Get Conversation Diagnostics

     Return durable per-stage diagnostic events for a conversation.

    Args:
        conversation_id (UUID):
        limit (int | Unset):  Default: 500.
        event_type (None | str | Unset):
        stage (None | str | Unset):
        severity (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConversationDiagnosticsResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        conversation_id=conversation_id,
        limit=limit,
        event_type=event_type,
        stage=stage,
        severity=severity,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    conversation_id: UUID,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 500,
    event_type: None | str | Unset = UNSET,
    stage: None | str | Unset = UNSET,
    severity: None | str | Unset = UNSET,
) -> ConversationDiagnosticsResponse | HTTPValidationError | None:
    """Get Conversation Diagnostics

     Return durable per-stage diagnostic events for a conversation.

    Args:
        conversation_id (UUID):
        limit (int | Unset):  Default: 500.
        event_type (None | str | Unset):
        stage (None | str | Unset):
        severity (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConversationDiagnosticsResponse | HTTPValidationError
    """

    return sync_detailed(
        conversation_id=conversation_id,
        client=client,
        limit=limit,
        event_type=event_type,
        stage=stage,
        severity=severity,
    ).parsed


async def asyncio_detailed(
    conversation_id: UUID,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 500,
    event_type: None | str | Unset = UNSET,
    stage: None | str | Unset = UNSET,
    severity: None | str | Unset = UNSET,
) -> Response[ConversationDiagnosticsResponse | HTTPValidationError]:
    """Get Conversation Diagnostics

     Return durable per-stage diagnostic events for a conversation.

    Args:
        conversation_id (UUID):
        limit (int | Unset):  Default: 500.
        event_type (None | str | Unset):
        stage (None | str | Unset):
        severity (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConversationDiagnosticsResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        conversation_id=conversation_id,
        limit=limit,
        event_type=event_type,
        stage=stage,
        severity=severity,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    conversation_id: UUID,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 500,
    event_type: None | str | Unset = UNSET,
    stage: None | str | Unset = UNSET,
    severity: None | str | Unset = UNSET,
) -> ConversationDiagnosticsResponse | HTTPValidationError | None:
    """Get Conversation Diagnostics

     Return durable per-stage diagnostic events for a conversation.

    Args:
        conversation_id (UUID):
        limit (int | Unset):  Default: 500.
        event_type (None | str | Unset):
        stage (None | str | Unset):
        severity (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConversationDiagnosticsResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            conversation_id=conversation_id,
            client=client,
            limit=limit,
            event_type=event_type,
            stage=stage,
            severity=severity,
        )
    ).parsed
