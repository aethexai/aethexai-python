from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="PaymentMethodCard")


@_attrs_define
class PaymentMethodCard:
    """Trimmed card view for the portal billing card panel.

    No PAN, no CVV, no full card number — Stripe never returns those
    to us. Last 4 + brand + expiry are enough to render
    "Visa ending 4242, expires 12/2027".

        Attributes:
            id (str):
            brand (None | str | Unset):
            exp_month (int | None | Unset):
            exp_year (int | None | Unset):
            is_default (bool | Unset): True for the PM at ``customer.invoice_settings.default_payment_method`` — the card
                Stripe will charge for renewals / proration / dunning retries. Portal uses this to render the 'Default' badge
                accurately rather than guessing by list position. Default: False.
            last4 (None | str | Unset):
    """

    id: str
    brand: None | str | Unset = UNSET
    exp_month: int | None | Unset = UNSET
    exp_year: int | None | Unset = UNSET
    is_default: bool | Unset = False
    last4: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        brand: None | str | Unset
        if isinstance(self.brand, Unset):
            brand = UNSET
        else:
            brand = self.brand

        exp_month: int | None | Unset
        if isinstance(self.exp_month, Unset):
            exp_month = UNSET
        else:
            exp_month = self.exp_month

        exp_year: int | None | Unset
        if isinstance(self.exp_year, Unset):
            exp_year = UNSET
        else:
            exp_year = self.exp_year

        is_default = self.is_default

        last4: None | str | Unset
        if isinstance(self.last4, Unset):
            last4 = UNSET
        else:
            last4 = self.last4

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand
        if exp_month is not UNSET:
            field_dict["exp_month"] = exp_month
        if exp_year is not UNSET:
            field_dict["exp_year"] = exp_year
        if is_default is not UNSET:
            field_dict["is_default"] = is_default
        if last4 is not UNSET:
            field_dict["last4"] = last4

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_brand(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        brand = _parse_brand(d.pop("brand", UNSET))

        def _parse_exp_month(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        exp_month = _parse_exp_month(d.pop("exp_month", UNSET))

        def _parse_exp_year(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        exp_year = _parse_exp_year(d.pop("exp_year", UNSET))

        is_default = d.pop("is_default", UNSET)

        def _parse_last4(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last4 = _parse_last4(d.pop("last4", UNSET))

        payment_method_card = cls(
            id=id,
            brand=brand,
            exp_month=exp_month,
            exp_year=exp_year,
            is_default=is_default,
            last4=last4,
        )

        payment_method_card.additional_properties = d
        return payment_method_card

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
