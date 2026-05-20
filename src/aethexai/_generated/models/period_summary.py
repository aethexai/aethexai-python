from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="PeriodSummary")


@_attrs_define
class PeriodSummary:
    """Snapshot of the current billing period: start/end + the
    grant/used/remaining decomposition the portal billing card needs.

    ``credits_granted`` is the **plan's monthly allocation**, not a
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
    the gap as "ops adjustment" if needed.

    ``credits_remaining`` mirrors ``Tenant.credit_balance`` so the portal
    can highlight a single source-of-truth number; it can exceed
    ``credits_granted`` after a PAYG top-up.

        Attributes:
            credits_granted (str):
            credits_remaining (str):
            credits_used (str):
            ends_at (datetime.datetime):
            started_at (datetime.datetime):
    """

    credits_granted: str
    credits_remaining: str
    credits_used: str
    ends_at: datetime.datetime
    started_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        credits_granted = self.credits_granted

        credits_remaining = self.credits_remaining

        credits_used = self.credits_used

        ends_at = self.ends_at.isoformat()

        started_at = self.started_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "credits_granted": credits_granted,
                "credits_remaining": credits_remaining,
                "credits_used": credits_used,
                "ends_at": ends_at,
                "started_at": started_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        credits_granted = d.pop("credits_granted")

        credits_remaining = d.pop("credits_remaining")

        credits_used = d.pop("credits_used")

        ends_at = isoparse(d.pop("ends_at"))

        started_at = isoparse(d.pop("started_at"))

        period_summary = cls(
            credits_granted=credits_granted,
            credits_remaining=credits_remaining,
            credits_used=credits_used,
            ends_at=ends_at,
            started_at=started_at,
        )

        period_summary.additional_properties = d
        return period_summary

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
