from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="PlanInfo")


@_attrs_define
class PlanInfo:
    """Compact plan view used inside the balance response. The full
    catalogue lives at ``GET /billing/plans`` for plan-picker UIs.

        Attributes:
            monthly_credits (str):
            monthly_price_usd (str):
            name (str):
            slug (str):
            yearly_price_usd (None | str | Unset):
    """

    monthly_credits: str
    monthly_price_usd: str
    name: str
    slug: str
    yearly_price_usd: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        monthly_credits = self.monthly_credits

        monthly_price_usd = self.monthly_price_usd

        name = self.name

        slug = self.slug

        yearly_price_usd: None | str | Unset
        if isinstance(self.yearly_price_usd, Unset):
            yearly_price_usd = UNSET
        else:
            yearly_price_usd = self.yearly_price_usd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "monthly_credits": monthly_credits,
                "monthly_price_usd": monthly_price_usd,
                "name": name,
                "slug": slug,
            }
        )
        if yearly_price_usd is not UNSET:
            field_dict["yearly_price_usd"] = yearly_price_usd

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        monthly_credits = d.pop("monthly_credits")

        monthly_price_usd = d.pop("monthly_price_usd")

        name = d.pop("name")

        slug = d.pop("slug")

        def _parse_yearly_price_usd(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        yearly_price_usd = _parse_yearly_price_usd(d.pop("yearly_price_usd", UNSET))

        plan_info = cls(
            monthly_credits=monthly_credits,
            monthly_price_usd=monthly_price_usd,
            name=name,
            slug=slug,
            yearly_price_usd=yearly_price_usd,
        )

        plan_info.additional_properties = d
        return plan_info

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
