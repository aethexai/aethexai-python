from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="TranscriptionResponse")


@_attrs_define
class TranscriptionResponse:
    """
    Attributes:
        id (str):
        created_at (None | str | Unset):
        duration_seconds (float | None | Unset):
        language (None | str | Unset):
        processing_time_ms (int | None | Unset):
        segments (list[Any] | Unset):
        status (str | Unset):  Default: 'completed'.
        text (str | Unset):  Default: ''.
    """

    id: str
    created_at: None | str | Unset = UNSET
    duration_seconds: float | None | Unset = UNSET
    language: None | str | Unset = UNSET
    processing_time_ms: int | None | Unset = UNSET
    segments: list[Any] | Unset = UNSET
    status: str | Unset = "completed"
    text: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        processing_time_ms: int | None | Unset
        if isinstance(self.processing_time_ms, Unset):
            processing_time_ms = UNSET
        else:
            processing_time_ms = self.processing_time_ms

        segments: list[Any] | Unset = UNSET
        if not isinstance(self.segments, Unset):
            segments = self.segments

        status = self.status

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if duration_seconds is not UNSET:
            field_dict["duration_seconds"] = duration_seconds
        if language is not UNSET:
            field_dict["language"] = language
        if processing_time_ms is not UNSET:
            field_dict["processing_time_ms"] = processing_time_ms
        if segments is not UNSET:
            field_dict["segments"] = segments
        if status is not UNSET:
            field_dict["status"] = status
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

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

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        def _parse_processing_time_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        processing_time_ms = _parse_processing_time_ms(d.pop("processing_time_ms", UNSET))

        segments = cast(list[Any], d.pop("segments", UNSET))

        status = d.pop("status", UNSET)

        text = d.pop("text", UNSET)

        transcription_response = cls(
            id=id,
            created_at=created_at,
            duration_seconds=duration_seconds,
            language=language,
            processing_time_ms=processing_time_ms,
            segments=segments,
            status=status,
            text=text,
        )

        transcription_response.additional_properties = d
        return transcription_response

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
