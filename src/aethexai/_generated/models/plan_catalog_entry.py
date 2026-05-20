from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="PlanCatalogEntry")


@_attrs_define
class PlanCatalogEntry:
    """A single tier in the public plan catalogue.

    ``yearly_price_usd`` is null on tiers without a yearly variant
    (the free trial). Portal toggles between monthly and yearly
    pricing only on tiers where it's non-null.

    ``is_trial`` flips the renewal-job behavior: trial plans grant
    credits once at signup and never refill. Currently only the free
    plan is a trial.

        Attributes:
            monthly_credits (str):
            monthly_price_usd (str):
            name (str):
            slug (str):
            features (list[str] | Unset):
            is_trial (bool | Unset):  Default: False.
            yearly_price_usd (None | str | Unset):
    """

    monthly_credits: str
    monthly_price_usd: str
    name: str
    slug: str
    features: list[str] | Unset = UNSET
    is_trial: bool | Unset = False
    yearly_price_usd: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        monthly_credits = self.monthly_credits

        monthly_price_usd = self.monthly_price_usd

        name = self.name

        slug = self.slug

        features: list[str] | Unset = UNSET
        if not isinstance(self.features, Unset):
            features = self.features

        is_trial = self.is_trial

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
        if features is not UNSET:
            field_dict["features"] = features
        if is_trial is not UNSET:
            field_dict["is_trial"] = is_trial
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

        features = cast(list[str], d.pop("features", UNSET))

        is_trial = d.pop("is_trial", UNSET)

        def _parse_yearly_price_usd(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        yearly_price_usd = _parse_yearly_price_usd(d.pop("yearly_price_usd", UNSET))

        plan_catalog_entry = cls(
            monthly_credits=monthly_credits,
            monthly_price_usd=monthly_price_usd,
            name=name,
            slug=slug,
            features=features,
            is_trial=is_trial,
            yearly_price_usd=yearly_price_usd,
        )

        plan_catalog_entry.additional_properties = d
        return plan_catalog_entry

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
