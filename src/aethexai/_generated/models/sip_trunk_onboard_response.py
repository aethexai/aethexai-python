from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.phone_number_response import PhoneNumberResponse
    from ..models.sip_trunk_response import SipTrunkResponse


T = TypeVar("T", bound="SipTrunkOnboardResponse")


@_attrs_define
class SipTrunkOnboardResponse:
    """
    Attributes:
        phone_numbers (list[PhoneNumberResponse]):
        trunk (SipTrunkResponse):
        tenant_default_set (bool | Unset):  Default: False.
    """

    phone_numbers: list[PhoneNumberResponse]
    trunk: SipTrunkResponse
    tenant_default_set: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.phone_number_response import PhoneNumberResponse
        from ..models.sip_trunk_response import SipTrunkResponse

        phone_numbers = []
        for phone_numbers_item_data in self.phone_numbers:
            phone_numbers_item = phone_numbers_item_data.to_dict()
            phone_numbers.append(phone_numbers_item)

        trunk = self.trunk.to_dict()

        tenant_default_set = self.tenant_default_set

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "phone_numbers": phone_numbers,
                "trunk": trunk,
            }
        )
        if tenant_default_set is not UNSET:
            field_dict["tenant_default_set"] = tenant_default_set

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_number_response import PhoneNumberResponse
        from ..models.sip_trunk_response import SipTrunkResponse

        d = dict(src_dict)
        phone_numbers = []
        _phone_numbers = d.pop("phone_numbers")
        for phone_numbers_item_data in _phone_numbers:
            phone_numbers_item = PhoneNumberResponse.from_dict(phone_numbers_item_data)

            phone_numbers.append(phone_numbers_item)

        trunk = SipTrunkResponse.from_dict(d.pop("trunk"))

        tenant_default_set = d.pop("tenant_default_set", UNSET)

        sip_trunk_onboard_response = cls(
            phone_numbers=phone_numbers,
            trunk=trunk,
            tenant_default_set=tenant_default_set,
        )

        sip_trunk_onboard_response.additional_properties = d
        return sip_trunk_onboard_response

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
