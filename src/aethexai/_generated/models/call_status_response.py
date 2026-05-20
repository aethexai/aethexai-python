from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.call_status_response_provider import CallStatusResponseProvider
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="CallStatusResponse")


@_attrs_define
class CallStatusResponse:
    """
    Attributes:
        provider (CallStatusResponseProvider):
        status (str):
        duration_s (float | None | Unset):
    """

    provider: CallStatusResponseProvider
    status: str
    duration_s: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider.value

        status = self.status

        duration_s: float | None | Unset
        if isinstance(self.duration_s, Unset):
            duration_s = UNSET
        else:
            duration_s = self.duration_s

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "status": status,
            }
        )
        if duration_s is not UNSET:
            field_dict["duration_s"] = duration_s

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider = CallStatusResponseProvider(d.pop("provider"))

        status = d.pop("status")

        def _parse_duration_s(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        duration_s = _parse_duration_s(d.pop("duration_s", UNSET))

        call_status_response = cls(
            provider=provider,
            status=status,
            duration_s=duration_s,
        )

        call_status_response.additional_properties = d
        return call_status_response

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
