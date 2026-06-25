from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.dunning_state import DunningState
    from ..models.payg_state import PaygState
    from ..models.period_summary import PeriodSummary
    from ..models.plan_info import PlanInfo


T = TypeVar("T", bound="BalanceResponse")


@_attrs_define
class BalanceResponse:
    """``GET /billing/balance`` payload. Renders the portal billing card without a second round-trip:
    balance, current plan, and the period decomposition. ``estimated_minutes_remaining`` is derived (1 credit ≈ 1 agent
    minute) so the UI doesn't have to know the conversion ratio.

        Attributes:
            credit_balance (str): Authoritative balance from ``.credit_balance``. Decimal-string to preserve precision for
                JavaScript clients.
            estimated_minutes_remaining (int): Approximate agent-call minutes the current balance covers, computed at the
                standard 1 credit per minute conversion.
            period (PeriodSummary): Snapshot of the current billing period: start/end + the
                grant/used/remaining decomposition the portal billing card needs. ``credits_granted`` is the **plan's monthly
                allocation**, not a
                sum of ledger grant rows in the current period. A tenant who
                upgraded mid-period or received a manual ``adjustment`` will see
                this field reflect the plan tier, not the literal credits that
                landed in the ledger. The portal renders this as "your plan
                includes N", not "you received N this period."

                ``credits_used`` is the sum of ``tx_type='usage_deduction'`` ledger
                entries since ``started_at``. Excluded from this stat:

                 * ``plan_credit`` (signup seed)
                 * ``plan_renewal`` (monthly / yearly grant)
                 * ``adjustment`` (ops-driven manual changes; rare)
                 * future PAYG top-ups (will use a distinct ``tx_type``)

                Negative ``adjustment`` entries reduce ``credit_balance`` without
                incrementing ``credits_used`` — the portal can detect this when
                ``credits_granted - credits_used > credits_remaining`` and explain
                the gap as "ops adjustment" if needed. ``credits_remaining`` mirrors ``Tenant.credit_balance`` so the portal
                can highlight a single source-of-truth number; it can exceed
                ``credits_granted`` after a PAYG top-up.
            plan (PlanInfo): Compact plan view used inside the balance response. The full
                catalogue lives at ``GET /billing/plans`` for plan-picker UIs.
            billing_mode (str | Unset): Billing mode for the tenant: ``auto_charge`` (default; charged to the card on file) or ``invoice`` (pay by invoice / wire / ACH). Default: 'auto_charge'.
            dunning (DunningState | None | Unset): Stripe dunning timeline when ``payment_status='past_due'``. ``None`` for
                healthy / canceled tenants and for tenants we couldn't reach Stripe for at request time.
            payg_state (None | PaygState | Unset): Pay-as-you-go state when ``credit_balance < 0``. ``None`` when balance is
                non-negative (no overage).
            payment_status (str | Unset): Tenant payment_status: ``active`` (healthy), ``past_due`` (card declined; Stripe
                is retrying), or ``canceled`` (Stripe gave up retrying or chargeback). Surfaced here so the portal can render a
                single billing-card without a second round-trip for the status banner. Default: 'active'.
            subscription_interval (None | str | Unset): Payment cadence on the tenant's active Stripe subscription:
                ``monthly``, ``yearly``, or ``null`` (free tier or no paid sub). Surfaced so the portal can label the price hero
                correctly ('$5/mo' vs '$50/yr') and the plan picker can enable monthly↔yearly switching without a blind round-
                trip. Distinct from the GRANT cadence (always monthly today), which lives on ``.billing_interval`` and isn't
                exposed to the portal.
    """

    credit_balance: str
    estimated_minutes_remaining: int
    period: PeriodSummary
    plan: PlanInfo
    billing_mode: str | Unset = "auto_charge"
    dunning: DunningState | None | Unset = UNSET
    payg_state: None | PaygState | Unset = UNSET
    payment_status: str | Unset = "active"
    subscription_interval: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dunning_state import DunningState
        from ..models.payg_state import PaygState
        from ..models.period_summary import PeriodSummary
        from ..models.plan_info import PlanInfo

        credit_balance = self.credit_balance

        estimated_minutes_remaining = self.estimated_minutes_remaining

        period = self.period.to_dict()

        plan = self.plan.to_dict()

        billing_mode = self.billing_mode

        dunning: dict[str, Any] | None | Unset
        if isinstance(self.dunning, Unset):
            dunning = UNSET
        elif isinstance(self.dunning, DunningState):
            dunning = self.dunning.to_dict()
        else:
            dunning = self.dunning

        payg_state: dict[str, Any] | None | Unset
        if isinstance(self.payg_state, Unset):
            payg_state = UNSET
        elif isinstance(self.payg_state, PaygState):
            payg_state = self.payg_state.to_dict()
        else:
            payg_state = self.payg_state

        payment_status = self.payment_status

        subscription_interval: None | str | Unset
        if isinstance(self.subscription_interval, Unset):
            subscription_interval = UNSET
        else:
            subscription_interval = self.subscription_interval

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "credit_balance": credit_balance,
                "estimated_minutes_remaining": estimated_minutes_remaining,
                "period": period,
                "plan": plan,
            }
        )
        if billing_mode is not UNSET:
            field_dict["billing_mode"] = billing_mode
        if dunning is not UNSET:
            field_dict["dunning"] = dunning
        if payg_state is not UNSET:
            field_dict["payg_state"] = payg_state
        if payment_status is not UNSET:
            field_dict["payment_status"] = payment_status
        if subscription_interval is not UNSET:
            field_dict["subscription_interval"] = subscription_interval

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dunning_state import DunningState
        from ..models.payg_state import PaygState
        from ..models.period_summary import PeriodSummary
        from ..models.plan_info import PlanInfo

        d = dict(src_dict)
        credit_balance = d.pop("credit_balance")

        estimated_minutes_remaining = d.pop("estimated_minutes_remaining")

        period = PeriodSummary.from_dict(d.pop("period"))

        plan = PlanInfo.from_dict(d.pop("plan"))

        billing_mode = d.pop("billing_mode", UNSET)

        def _parse_dunning(data: object) -> DunningState | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dunning_type_0 = DunningState.from_dict(data)

                return dunning_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DunningState | None | Unset, data)

        dunning = _parse_dunning(d.pop("dunning", UNSET))

        def _parse_payg_state(data: object) -> None | PaygState | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                payg_state_type_0 = PaygState.from_dict(data)

                return payg_state_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PaygState | Unset, data)

        payg_state = _parse_payg_state(d.pop("payg_state", UNSET))

        payment_status = d.pop("payment_status", UNSET)

        def _parse_subscription_interval(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        subscription_interval = _parse_subscription_interval(d.pop("subscription_interval", UNSET))

        balance_response = cls(
            credit_balance=credit_balance,
            estimated_minutes_remaining=estimated_minutes_remaining,
            period=period,
            plan=plan,
            billing_mode=billing_mode,
            dunning=dunning,
            payg_state=payg_state,
            payment_status=payment_status,
            subscription_interval=subscription_interval,
        )

        balance_response.additional_properties = d
        return balance_response

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
