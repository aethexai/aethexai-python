from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.usage_by_resource_entry import UsageByResourceEntry


T = TypeVar("T", bound="UsageSummaryByResourceType")


@_attrs_define
class UsageSummaryByResourceType:
    """ """

    additional_properties: dict[str, UsageByResourceEntry] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_by_resource_entry import UsageByResourceEntry

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_by_resource_entry import UsageByResourceEntry

        d = dict(src_dict)
        usage_summary_by_resource_type = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = UsageByResourceEntry.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        usage_summary_by_resource_type.additional_properties = additional_properties
        return usage_summary_by_resource_type

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> UsageByResourceEntry:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: UsageByResourceEntry) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
