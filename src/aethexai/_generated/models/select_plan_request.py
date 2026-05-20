from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="SelectPlanRequest")


@_attrs_define
class SelectPlanRequest:
    """Optional body for ``POST /billing/plans/{slug}/select``.

    Defaults to monthly billing. Yearly is rejected with 400 if the
    requested plan has no yearly variant configured (currently the
    free trial). The interval drives which ``stripe_price_id`` the
    backend hands to ``create_subscription`` /
    ``update_subscription_price`` and which ``Stripe Price`` Stripe
    bills against.

        Attributes:
            interval (str | Unset):  Default: 'monthly'.
    """

    interval: str | Unset = "monthly"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        interval = self.interval

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if interval is not UNSET:
            field_dict["interval"] = interval

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        interval = d.pop("interval", UNSET)

        select_plan_request = cls(
            interval=interval,
        )

        select_plan_request.additional_properties = d
        return select_plan_request

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
