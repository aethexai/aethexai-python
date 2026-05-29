from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="PaygState")


@_attrs_define
class PaygState:
    """Pay-as-you-go (overage) accounting state for the current period. Surfaced when ``credit_balance < 0`` so the portal
    can render
    "X credits over · ~$Y will charge at the next $5 threshold". Tenants
    on ``has_payment_method=False`` see the same negative balance but
    can't be charged — the portal renders "Add a card to keep service
    running" instead.

        Attributes:
            pending_overage_credits (str): Absolute value of the negative balance, in credits. Always >= 0; the sign is
                implied (overage).
            pending_overage_usd (str): Pending overage in USD at the current PAYG rate (``PAYG_OVERAGE_RATE_USD_PER_MINUTE``
                = $0.065/credit today).
            threshold_credits (str): Credit threshold above which the next PAYG charge fires. Surfaced so the portal can
                render a 'next charge at X' progress.
            last_charge_at (datetime.datetime | None | Unset): Timestamp of the most recent successful PAYG charge.
    """

    pending_overage_credits: str
    pending_overage_usd: str
    threshold_credits: str
    last_charge_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pending_overage_credits = self.pending_overage_credits

        pending_overage_usd = self.pending_overage_usd

        threshold_credits = self.threshold_credits

        last_charge_at: None | str | Unset
        if isinstance(self.last_charge_at, Unset):
            last_charge_at = UNSET
        elif isinstance(self.last_charge_at, datetime.datetime):
            last_charge_at = self.last_charge_at.isoformat()
        else:
            last_charge_at = self.last_charge_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pending_overage_credits": pending_overage_credits,
                "pending_overage_usd": pending_overage_usd,
                "threshold_credits": threshold_credits,
            }
        )
        if last_charge_at is not UNSET:
            field_dict["last_charge_at"] = last_charge_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pending_overage_credits = d.pop("pending_overage_credits")

        pending_overage_usd = d.pop("pending_overage_usd")

        threshold_credits = d.pop("threshold_credits")

        def _parse_last_charge_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_charge_at_type_0 = isoparse(data)

                return last_charge_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_charge_at = _parse_last_charge_at(d.pop("last_charge_at", UNSET))

        payg_state = cls(
            pending_overage_credits=pending_overage_credits,
            pending_overage_usd=pending_overage_usd,
            threshold_credits=threshold_credits,
            last_charge_at=last_charge_at,
        )

        payg_state.additional_properties = d
        return payg_state

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
