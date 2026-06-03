from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="LogoutAllResponse")


@_attrs_define
class LogoutAllResponse:
    """
    Attributes:
        revoked_count (int | Unset):  Default: 0.
        success (bool | Unset):  Default: True.
    """

    revoked_count: int | Unset = 0
    success: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        revoked_count = self.revoked_count

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if revoked_count is not UNSET:
            field_dict["revoked_count"] = revoked_count
        if success is not UNSET:
            field_dict["success"] = success

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        revoked_count = d.pop("revoked_count", UNSET)

        success = d.pop("success", UNSET)

        logout_all_response = cls(
            revoked_count=revoked_count,
            success=success,
        )

        logout_all_response.additional_properties = d
        return logout_all_response

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
