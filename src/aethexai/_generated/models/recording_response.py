from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="RecordingResponse")


@_attrs_define
class RecordingResponse:
    """
    Attributes:
        call_id (str):
        id (str):
        storage_path (str | Unset): Internal object-store key; present today but
            will be absent once the backend removes the field (aethex#1007).
            Treat as opaque — do not rely on its value.
        created_at (None | str | Unset):
        duration_seconds (float | None | Unset):
        format_ (str | Unset):  Default: 'wav'.
        size_bytes (int | None | Unset):
        status (str | Unset):  Default: 'completed'.
    """

    call_id: str
    id: str
    created_at: None | str | Unset = UNSET
    storage_path: str | Unset = UNSET
    duration_seconds: float | None | Unset = UNSET
    format_: str | Unset = "wav"
    size_bytes: int | None | Unset = UNSET
    status: str | Unset = "completed"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call_id = self.call_id

        id = self.id

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        duration_seconds: float | None | Unset
        if isinstance(self.duration_seconds, Unset):
            duration_seconds = UNSET
        else:
            duration_seconds = self.duration_seconds

        format_ = self.format_

        size_bytes: int | None | Unset
        if isinstance(self.size_bytes, Unset):
            size_bytes = UNSET
        else:
            size_bytes = self.size_bytes

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call_id": call_id,
                "id": id,
            }
        )
        if self.storage_path is not UNSET:
            field_dict["storage_path"] = self.storage_path
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if duration_seconds is not UNSET:
            field_dict["duration_seconds"] = duration_seconds
        if format_ is not UNSET:
            field_dict["format"] = format_
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        call_id = d.pop("call_id")

        id = d.pop("id")

        storage_path = d.pop("storage_path", UNSET)

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_duration_seconds(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        duration_seconds = _parse_duration_seconds(d.pop("duration_seconds", UNSET))

        format_ = d.pop("format", UNSET)

        def _parse_size_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        size_bytes = _parse_size_bytes(d.pop("size_bytes", UNSET))

        status = d.pop("status", UNSET)

        recording_response = cls(
            call_id=call_id,
            id=id,
            storage_path=storage_path,
            created_at=created_at,
            duration_seconds=duration_seconds,
            format_=format_,
            size_bytes=size_bytes,
            status=status,
        )

        recording_response.additional_properties = d
        return recording_response

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
