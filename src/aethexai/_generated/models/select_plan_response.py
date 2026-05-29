from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="SelectPlanResponse")


@_attrs_define
class SelectPlanResponse:
    """``POST /billing/plans/{slug}/select`` payload.

    Returns the new state after the Stripe subscription create / update
    / scheduled cancellation. ``status`` is one of:

      * Stripe subscription status pass-through: ``active``,
        ``trialing``, ``incomplete`` (first-charge pending),
        ``past_due``, etc.
      * ``free`` -- already-free tenant with a saved payment method
        re-affirmed the free tier; no Stripe call was needed.
      * ``scheduled_cancellation`` -- voluntary downgrade from a paid
        tier to free. The Stripe sub stays active through the period
        the customer paid for; the portal renders "Cancellation
        scheduled for <period_end>" until the period-boundary
        ``customer.subscription.deleted`` webhook flips them to free.

    When ``status='incomplete'`` (declining first-charge under
    ``payment_behavior='default_incomplete'``) the response includes
    ``payment_intent_client_secret`` so the portal can call
    ``stripe.confirmCardPayment(client_secret)`` to recover within
    Stripe's 23-hour completion window. ``billing_plan`` does NOT
    advance to the new tier in this case; the customer's plan only
    changes after Stripe transitions the subscription to ``active``
    and fires ``customer.subscription.updated`` (which the webhook
    handler picks up to commit the plan).

        Attributes:
            plan_slug (str):
            status (str):
            awaiting_payment (bool | Unset): True when a paid->paid upgrade is held in Stripe's pending-updates state --
                subscription is still on the OLD price + slug pending the proration invoice payment. Status will read 'active'
                even in this case (the subscription itself is active, just on the old price). Portal should surface 'Complete
                payment to apply your upgrade' alongside the PaymentIntent confirmation modal. Default: False.
            payment_intent_client_secret (None | str | Unset): Stripe PaymentIntent client_secret for the first invoice.
                Present when status='incomplete'; pass to the portal to confirm the existing payment (do NOT create a new
                subscription on retry — that would double-bill).
            subscription_id (None | str | Unset):
    """

    plan_slug: str
    status: str
    awaiting_payment: bool | Unset = False
    payment_intent_client_secret: None | str | Unset = UNSET
    subscription_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan_slug = self.plan_slug

        status = self.status

        awaiting_payment = self.awaiting_payment

        payment_intent_client_secret: None | str | Unset
        if isinstance(self.payment_intent_client_secret, Unset):
            payment_intent_client_secret = UNSET
        else:
            payment_intent_client_secret = self.payment_intent_client_secret

        subscription_id: None | str | Unset
        if isinstance(self.subscription_id, Unset):
            subscription_id = UNSET
        else:
            subscription_id = self.subscription_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan_slug": plan_slug,
                "status": status,
            }
        )
        if awaiting_payment is not UNSET:
            field_dict["awaiting_payment"] = awaiting_payment
        if payment_intent_client_secret is not UNSET:
            field_dict["payment_intent_client_secret"] = payment_intent_client_secret
        if subscription_id is not UNSET:
            field_dict["subscription_id"] = subscription_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan_slug = d.pop("plan_slug")

        status = d.pop("status")

        awaiting_payment = d.pop("awaiting_payment", UNSET)

        def _parse_payment_intent_client_secret(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        payment_intent_client_secret = _parse_payment_intent_client_secret(
            d.pop("payment_intent_client_secret", UNSET)
        )

        def _parse_subscription_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        subscription_id = _parse_subscription_id(d.pop("subscription_id", UNSET))

        select_plan_response = cls(
            plan_slug=plan_slug,
            status=status,
            awaiting_payment=awaiting_payment,
            payment_intent_client_secret=payment_intent_client_secret,
            subscription_id=subscription_id,
        )

        select_plan_response.additional_properties = d
        return select_plan_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
