from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.payment_method_summary import PaymentMethodSummary


T = TypeVar("T", bound="PaymentMethodListResponse")


@_attrs_define
class PaymentMethodListResponse:
    """``GET /billing/payment-methods`` payload.

    Attributes:
        has_payment_method (bool): Cached ``vo_tenants.has_payment_method`` flag. True iff the tenant has at least one
            ``card`` or Stripe ``link`` payment method attached (the two PM types ``select_plan`` and the PAYG cron can
            charge). Used by the portal to gate the upgrade button: no payment method -> redirect to attach flow first.
        payment_methods (list[PaymentMethodSummary]):
    """

    has_payment_method: bool
    payment_methods: list[PaymentMethodSummary]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.payment_method_summary import PaymentMethodSummary

        has_payment_method = self.has_payment_method

        payment_methods = []
        for payment_methods_item_data in self.payment_methods:
            payment_methods_item = payment_methods_item_data.to_dict()
            payment_methods.append(payment_methods_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_payment_method": has_payment_method,
                "payment_methods": payment_methods,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.payment_method_summary import PaymentMethodSummary

        d = dict(src_dict)
        has_payment_method = d.pop("has_payment_method")

        payment_methods = []
        _payment_methods = d.pop("payment_methods")
        for payment_methods_item_data in _payment_methods:
            payment_methods_item = PaymentMethodSummary.from_dict(payment_methods_item_data)

            payment_methods.append(payment_methods_item)

        payment_method_list_response = cls(
            has_payment_method=has_payment_method,
            payment_methods=payment_methods,
        )

        payment_method_list_response.additional_properties = d
        return payment_method_list_response

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
