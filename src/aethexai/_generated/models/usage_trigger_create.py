from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="UsageTriggerCreate")


@_attrs_define
class UsageTriggerCreate:
    """
    Attributes:
        event_callback_url (str):
        resource_type (str):
        threshold_value (float | str):
        period (str | Unset):  Default: 'monthly'.
        threshold_type (str | Unset):  Default: 'count'.
    """

    event_callback_url: str
    resource_type: str
    threshold_value: float | str
    period: str | Unset = "monthly"
    threshold_type: str | Unset = "count"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_callback_url = self.event_callback_url

        resource_type = self.resource_type

        threshold_value: float | str
        threshold_value = self.threshold_value

        period = self.period

        threshold_type = self.threshold_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_callback_url": event_callback_url,
                "resource_type": resource_type,
                "threshold_value": threshold_value,
            }
        )
        if period is not UNSET:
            field_dict["period"] = period
        if threshold_type is not UNSET:
            field_dict["threshold_type"] = threshold_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        event_callback_url = d.pop("event_callback_url")

        resource_type = d.pop("resource_type")

        def _parse_threshold_value(data: object) -> float | str:
            return cast(float | str, data)

        threshold_value = _parse_threshold_value(d.pop("threshold_value"))

        period = d.pop("period", UNSET)

        threshold_type = d.pop("threshold_type", UNSET)

        usage_trigger_create = cls(
            event_callback_url=event_callback_url,
            resource_type=resource_type,
            threshold_value=threshold_value,
            period=period,
            threshold_type=threshold_type,
        )

        usage_trigger_create.additional_properties = d
        return usage_trigger_create

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
