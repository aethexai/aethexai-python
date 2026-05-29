from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import cast


def _get_kwargs(
    payment_method_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/v1/billing/payment-methods/{payment_method_id}".format(
            payment_method_id=quote(str(payment_method_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 204:
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
    payment_method_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    r"""Detach Tenant Payment Method

     Detach a payment method from the tenant's Stripe Customer. Ownership is verified server-side BEFORE
    the detach call. Stripe's
    detach endpoint takes only the PM id (no customer scope), so a
    leaked ``pm_*`` id from logs / dashboard transcripts / accidental
    client-side console output would otherwise let any
    portal-authenticated tenant nuke another tenant's PM. We
    retrieve the PM, compare ``pm.customer`` to the JWT-bound
    tenant's ``stripe_customer_id``, and 404 on mismatch (same
    response as a non-existent id, so a probe can't distinguish
    \"wrong tenant\" from \"doesn't exist\"). One extra ~100ms Stripe
    roundtrip on a user-initiated, infrequent path. The ``has_payment_method`` cache flag is updated by
    the
    ``payment_method.attached`` / ``.detached`` webhook handlers
    (which use Stripe's ``previous_attributes`` to resolve the owner
    when the post-detach event has ``customer=null``). The route does
    NOT touch the cache directly — Stripe is source of truth and
    webhooks are how we mirror it. On any Stripe-side error the route surfaces the SDK's curated
    ``StripeError.user_message`` if present, falling back to a
    generic message. Programming bugs (TypeError, AttributeError,
    etc.) propagate to the global handler instead of being silently
    served as 400s.

    Args:
        payment_method_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        payment_method_id=payment_method_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    payment_method_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    r"""Detach Tenant Payment Method

     Detach a payment method from the tenant's Stripe Customer. Ownership is verified server-side BEFORE
    the detach call. Stripe's
    detach endpoint takes only the PM id (no customer scope), so a
    leaked ``pm_*`` id from logs / dashboard transcripts / accidental
    client-side console output would otherwise let any
    portal-authenticated tenant nuke another tenant's PM. We
    retrieve the PM, compare ``pm.customer`` to the JWT-bound
    tenant's ``stripe_customer_id``, and 404 on mismatch (same
    response as a non-existent id, so a probe can't distinguish
    \"wrong tenant\" from \"doesn't exist\"). One extra ~100ms Stripe
    roundtrip on a user-initiated, infrequent path. The ``has_payment_method`` cache flag is updated by
    the
    ``payment_method.attached`` / ``.detached`` webhook handlers
    (which use Stripe's ``previous_attributes`` to resolve the owner
    when the post-detach event has ``customer=null``). The route does
    NOT touch the cache directly — Stripe is source of truth and
    webhooks are how we mirror it. On any Stripe-side error the route surfaces the SDK's curated
    ``StripeError.user_message`` if present, falling back to a
    generic message. Programming bugs (TypeError, AttributeError,
    etc.) propagate to the global handler instead of being silently
    served as 400s.

    Args:
        payment_method_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        payment_method_id=payment_method_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    payment_method_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    r"""Detach Tenant Payment Method

     Detach a payment method from the tenant's Stripe Customer. Ownership is verified server-side BEFORE
    the detach call. Stripe's
    detach endpoint takes only the PM id (no customer scope), so a
    leaked ``pm_*`` id from logs / dashboard transcripts / accidental
    client-side console output would otherwise let any
    portal-authenticated tenant nuke another tenant's PM. We
    retrieve the PM, compare ``pm.customer`` to the JWT-bound
    tenant's ``stripe_customer_id``, and 404 on mismatch (same
    response as a non-existent id, so a probe can't distinguish
    \"wrong tenant\" from \"doesn't exist\"). One extra ~100ms Stripe
    roundtrip on a user-initiated, infrequent path. The ``has_payment_method`` cache flag is updated by
    the
    ``payment_method.attached`` / ``.detached`` webhook handlers
    (which use Stripe's ``previous_attributes`` to resolve the owner
    when the post-detach event has ``customer=null``). The route does
    NOT touch the cache directly — Stripe is source of truth and
    webhooks are how we mirror it. On any Stripe-side error the route surfaces the SDK's curated
    ``StripeError.user_message`` if present, falling back to a
    generic message. Programming bugs (TypeError, AttributeError,
    etc.) propagate to the global handler instead of being silently
    served as 400s.

    Args:
        payment_method_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        payment_method_id=payment_method_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    payment_method_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    r"""Detach Tenant Payment Method

     Detach a payment method from the tenant's Stripe Customer. Ownership is verified server-side BEFORE
    the detach call. Stripe's
    detach endpoint takes only the PM id (no customer scope), so a
    leaked ``pm_*`` id from logs / dashboard transcripts / accidental
    client-side console output would otherwise let any
    portal-authenticated tenant nuke another tenant's PM. We
    retrieve the PM, compare ``pm.customer`` to the JWT-bound
    tenant's ``stripe_customer_id``, and 404 on mismatch (same
    response as a non-existent id, so a probe can't distinguish
    \"wrong tenant\" from \"doesn't exist\"). One extra ~100ms Stripe
    roundtrip on a user-initiated, infrequent path. The ``has_payment_method`` cache flag is updated by
    the
    ``payment_method.attached`` / ``.detached`` webhook handlers
    (which use Stripe's ``previous_attributes`` to resolve the owner
    when the post-detach event has ``customer=null``). The route does
    NOT touch the cache directly — Stripe is source of truth and
    webhooks are how we mirror it. On any Stripe-side error the route surfaces the SDK's curated
    ``StripeError.user_message`` if present, falling back to a
    generic message. Programming bugs (TypeError, AttributeError,
    etc.) propagate to the global handler instead of being silently
    served as 400s.

    Args:
        payment_method_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            payment_method_id=payment_method_id,
            client=client,
        )
    ).parsed
