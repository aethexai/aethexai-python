from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="DashboardOverview")


@_attrs_define
class DashboardOverview:
    """
    Attributes:
        tenant_id (str):
        active_api_keys (int | Unset):  Default: 0.
        requests_today (int | Unset):  Default: 0.
        total_api_keys (int | Unset):  Default: 0.
        total_calls (int | Unset):  Default: 0.
        total_requests (int | Unset):  Default: 0.
    """

    tenant_id: str
    active_api_keys: int | Unset = 0
    requests_today: int | Unset = 0
    total_api_keys: int | Unset = 0
    total_calls: int | Unset = 0
    total_requests: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tenant_id = self.tenant_id

        active_api_keys = self.active_api_keys

        requests_today = self.requests_today

        total_api_keys = self.total_api_keys

        total_calls = self.total_calls

        total_requests = self.total_requests

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tenant_id": tenant_id,
            }
        )
        if active_api_keys is not UNSET:
            field_dict["active_api_keys"] = active_api_keys
        if requests_today is not UNSET:
            field_dict["requests_today"] = requests_today
        if total_api_keys is not UNSET:
            field_dict["total_api_keys"] = total_api_keys
        if total_calls is not UNSET:
            field_dict["total_calls"] = total_calls
        if total_requests is not UNSET:
            field_dict["total_requests"] = total_requests

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tenant_id = d.pop("tenant_id")

        active_api_keys = d.pop("active_api_keys", UNSET)

        requests_today = d.pop("requests_today", UNSET)

        total_api_keys = d.pop("total_api_keys", UNSET)

        total_calls = d.pop("total_calls", UNSET)

        total_requests = d.pop("total_requests", UNSET)

        dashboard_overview = cls(
            tenant_id=tenant_id,
            active_api_keys=active_api_keys,
            requests_today=requests_today,
            total_api_keys=total_api_keys,
            total_calls=total_calls,
            total_requests=total_requests,
        )

        dashboard_overview.additional_properties = d
        return dashboard_overview

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
