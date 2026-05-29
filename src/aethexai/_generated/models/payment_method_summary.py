from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.payment_method_summary_type import PaymentMethodSummaryType
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="PaymentMethodSummary")


@_attrs_define
class PaymentMethodSummary:
    """Trimmed PaymentMethod view for the portal billing panel. Covers both card and Stripe Link PMs. No PAN, no CVV, no
    full card
    number, Stripe never returns those to us. For cards the brand,
    last4, and expiry fields populate; for Link PMs those are null and
    ``link_email`` carries the Link account's email so the portal can
    render "Link account user@example.com".

        Attributes:
            id (str):
            type_ (PaymentMethodSummaryType): Stripe PaymentMethod ``type``. ``card`` and ``link`` are the two values the
                portal can attach today; other Stripe types (klarna, cashapp, amazon_pay) are not allowed by the SetupIntent /
                Subscription configuration because they do not support off-session recurring charges.
            brand (None | str | Unset):
            exp_month (int | None | Unset):
            exp_year (int | None | Unset):
            is_default (bool | Unset): True for the PM at ``customer.invoice_settings.default_payment_method``, the PM
                Stripe will charge for renewals / proration / dunning retries. Portal uses this to render the 'Default' badge
                accurately rather than guessing by list position. Default: False.
            last4 (None | str | Unset):
            link_email (None | str | Unset): Email associated with the Stripe Link PaymentMethod. Null for non-Link PMs.
            wallet_type (None | str | Unset): Wallet identifier for card PMs created via a digital wallet (apple_pay,
                google_pay, samsung_pay, link). Null for non-wallet cards and non-card PMs. Lets the portal render 'Apple Pay' /
                'Google Pay' instead of 'Visa ****1234' for tokenized wallet cards (Stripe surfaces these as ``type=card`` with
                ``card.wallet.type`` set).
    """

    id: str
    type_: PaymentMethodSummaryType
    brand: None | str | Unset = UNSET
    exp_month: int | None | Unset = UNSET
    exp_year: int | None | Unset = UNSET
    is_default: bool | Unset = False
    last4: None | str | Unset = UNSET
    link_email: None | str | Unset = UNSET
    wallet_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_.value

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

        link_email: None | str | Unset
        if isinstance(self.link_email, Unset):
            link_email = UNSET
        else:
            link_email = self.link_email

        wallet_type: None | str | Unset
        if isinstance(self.wallet_type, Unset):
            wallet_type = UNSET
        else:
            wallet_type = self.wallet_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
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
        if link_email is not UNSET:
            field_dict["link_email"] = link_email
        if wallet_type is not UNSET:
            field_dict["wallet_type"] = wallet_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = PaymentMethodSummaryType(d.pop("type"))

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

        def _parse_link_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        link_email = _parse_link_email(d.pop("link_email", UNSET))

        def _parse_wallet_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        wallet_type = _parse_wallet_type(d.pop("wallet_type", UNSET))

        payment_method_summary = cls(
            id=id,
            type_=type_,
            brand=brand,
            exp_month=exp_month,
            exp_year=exp_year,
            is_default=is_default,
            last4=last4,
            link_email=link_email,
            wallet_type=wallet_type,
        )

        payment_method_summary.additional_properties = d
        return payment_method_summary

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
