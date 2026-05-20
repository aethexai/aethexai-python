from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/twilio/transfer-status",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if response.status_code == 200:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any]:
    r"""Twilio Transfer Status

     Per-call StatusCallback for the transferee leg of a Conference transfer.

    ``_execute_twilio_transfer`` configures the outbound transferee dial
    with ``StatusCallback={this URL}?caller_sid=<original caller call_sid>``.
    Twilio POSTs here once the outbound leg reaches a terminal state
    (``completed`` if the transferee answered and the call later ended,
    or one of ``no-answer`` / ``busy`` / ``failed`` / ``canceled``).

    On a *failure* status, the caller is still in the Conference room
    listening to ``waitUrl`` music with no live counterpart. We POST
    ``<Hangup/>`` to the caller's leg via ``/Calls/{call_sid}.json`` so
    the conference ends. Without this the caller could hold a paid leg
    open until Twilio's default conference timeout (4 hours).

    On ``completed`` the transferee did connect at some point; the
    ``endConferenceOnExit=\"true\"`` attribute on the transferee's
    Conference TwiML already collapsed the room when they left, so no
    cleanup is needed.

    Signature is verified against the per-tenant auth_token resolved
    from the form's ``AccountSid`` (same path as the inbound webhook).
    Without verification an attacker who guessed a public ``caller_sid``
    could forge a ``no-answer`` to hang up active transfers.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any]:
    r"""Twilio Transfer Status

     Per-call StatusCallback for the transferee leg of a Conference transfer.

    ``_execute_twilio_transfer`` configures the outbound transferee dial
    with ``StatusCallback={this URL}?caller_sid=<original caller call_sid>``.
    Twilio POSTs here once the outbound leg reaches a terminal state
    (``completed`` if the transferee answered and the call later ended,
    or one of ``no-answer`` / ``busy`` / ``failed`` / ``canceled``).

    On a *failure* status, the caller is still in the Conference room
    listening to ``waitUrl`` music with no live counterpart. We POST
    ``<Hangup/>`` to the caller's leg via ``/Calls/{call_sid}.json`` so
    the conference ends. Without this the caller could hold a paid leg
    open until Twilio's default conference timeout (4 hours).

    On ``completed`` the transferee did connect at some point; the
    ``endConferenceOnExit=\"true\"`` attribute on the transferee's
    Conference TwiML already collapsed the room when they left, so no
    cleanup is needed.

    Signature is verified against the per-tenant auth_token resolved
    from the form's ``AccountSid`` (same path as the inbound webhook).
    Without verification an attacker who guessed a public ``caller_sid``
    could forge a ``no-answer`` to hang up active transfers.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
