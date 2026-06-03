from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="UsageTriggerResponse")


@_attrs_define
class UsageTriggerResponse:
    """
    Attributes:
        event_callback_url (str):
        id (str):
        resource_type (str):
        threshold_value (str):
        created_at (None | str | Unset):
        is_active (bool | Unset):  Default: True.
        last_fired_at (datetime.datetime | None | Unset):
        period (str | Unset):  Default: 'monthly'.
        threshold_type (str | Unset):  Default: 'count'.
    """

    event_callback_url: str
    id: str
    resource_type: str
    threshold_value: str
    created_at: None | str | Unset = UNSET
    is_active: bool | Unset = True
    last_fired_at: datetime.datetime | None | Unset = UNSET
    period: str | Unset = "monthly"
    threshold_type: str | Unset = "count"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_callback_url = self.event_callback_url

        id = self.id

        resource_type = self.resource_type

        threshold_value = self.threshold_value

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        is_active = self.is_active

        last_fired_at: None | str | Unset
        if isinstance(self.last_fired_at, Unset):
            last_fired_at = UNSET
        elif isinstance(self.last_fired_at, datetime.datetime):
            last_fired_at = self.last_fired_at.isoformat()
        else:
            last_fired_at = self.last_fired_at

        period = self.period

        threshold_type = self.threshold_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_callback_url": event_callback_url,
                "id": id,
                "resource_type": resource_type,
                "threshold_value": threshold_value,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if last_fired_at is not UNSET:
            field_dict["last_fired_at"] = last_fired_at
        if period is not UNSET:
            field_dict["period"] = period
        if threshold_type is not UNSET:
            field_dict["threshold_type"] = threshold_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        event_callback_url = d.pop("event_callback_url")

        id = d.pop("id")

        resource_type = d.pop("resource_type")

        threshold_value = d.pop("threshold_value")

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        is_active = d.pop("is_active", UNSET)

        def _parse_last_fired_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_fired_at_type_0 = isoparse(data)

                return last_fired_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_fired_at = _parse_last_fired_at(d.pop("last_fired_at", UNSET))

        period = d.pop("period", UNSET)

        threshold_type = d.pop("threshold_type", UNSET)

        usage_trigger_response = cls(
            event_callback_url=event_callback_url,
            id=id,
            resource_type=resource_type,
            threshold_value=threshold_value,
            created_at=created_at,
            is_active=is_active,
            last_fired_at=last_fired_at,
            period=period,
            threshold_type=threshold_type,
        )

        usage_trigger_response.additional_properties = d
        return usage_trigger_response

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
