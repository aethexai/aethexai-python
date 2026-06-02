from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.small_web_rtc_patch_request import SmallWebRTCPatchRequest
from typing import cast


def _get_kwargs(
    session_id: str,
    *,
    body: SmallWebRTCPatchRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/conversation/{session_id}/ice".format(
            session_id=quote(str(session_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if 200 <= response.status_code < 300:
        if not response.content:
            return None
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: SmallWebRTCPatchRequest,
) -> Response[Any | HTTPValidationError]:
    """Ice Candidate

     Handle ICE candidate trickle. Authenticated, quota-exempt signaling. ICE trickle is time-sensitive
    and
    can be high volume, so the rate-limiter middleware does not charge it
    against tenant API RPM, but callers must still present a valid
    ``calls:write`` API key.

    Args:
        session_id (str):
        body (SmallWebRTCPatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: SmallWebRTCPatchRequest,
) -> Any | HTTPValidationError | None:
    """Ice Candidate

     Handle ICE candidate trickle. Authenticated, quota-exempt signaling. ICE trickle is time-sensitive
    and
    can be high volume, so the rate-limiter middleware does not charge it
    against tenant API RPM, but callers must still present a valid
    ``calls:write`` API key.

    Args:
        session_id (str):
        body (SmallWebRTCPatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: SmallWebRTCPatchRequest,
) -> Response[Any | HTTPValidationError]:
    """Ice Candidate

     Handle ICE candidate trickle. Authenticated, quota-exempt signaling. ICE trickle is time-sensitive
    and
    can be high volume, so the rate-limiter middleware does not charge it
    against tenant API RPM, but callers must still present a valid
    ``calls:write`` API key.

    Args:
        session_id (str):
        body (SmallWebRTCPatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: SmallWebRTCPatchRequest,
) -> Any | HTTPValidationError | None:
    """Ice Candidate

     Handle ICE candidate trickle. Authenticated, quota-exempt signaling. ICE trickle is time-sensitive
    and
    can be high volume, so the rate-limiter middleware does not charge it
    against tenant API RPM, but callers must still present a valid
    ``calls:write`` API key.

    Args:
        session_id (str):
        body (SmallWebRTCPatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
            body=body,
        )
    ).parsed
