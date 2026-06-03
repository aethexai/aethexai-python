from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="UsageDailyEntry")


@_attrs_define
class UsageDailyEntry:
    """
    Attributes:
        count (int):
        date (str):
        audio_seconds (float | Unset):  Default: 0.0.
        completion_tokens (int | Unset):  Default: 0.
        input_characters (int | Unset):  Default: 0.
        prompt_tokens (int | Unset):  Default: 0.
        request_duration_ms (int | Unset):  Default: 0.
        total_tokens (int | Unset):  Default: 0.
        voice_seconds (float | Unset):  Default: 0.0.
    """

    count: int
    date: str
    audio_seconds: float | Unset = 0.0
    completion_tokens: int | Unset = 0
    input_characters: int | Unset = 0
    prompt_tokens: int | Unset = 0
    request_duration_ms: int | Unset = 0
    total_tokens: int | Unset = 0
    voice_seconds: float | Unset = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        date = self.date

        audio_seconds = self.audio_seconds

        completion_tokens = self.completion_tokens

        input_characters = self.input_characters

        prompt_tokens = self.prompt_tokens

        request_duration_ms = self.request_duration_ms

        total_tokens = self.total_tokens

        voice_seconds = self.voice_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "date": date,
            }
        )
        if audio_seconds is not UNSET:
            field_dict["audio_seconds"] = audio_seconds
        if completion_tokens is not UNSET:
            field_dict["completion_tokens"] = completion_tokens
        if input_characters is not UNSET:
            field_dict["input_characters"] = input_characters
        if prompt_tokens is not UNSET:
            field_dict["prompt_tokens"] = prompt_tokens
        if request_duration_ms is not UNSET:
            field_dict["request_duration_ms"] = request_duration_ms
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens
        if voice_seconds is not UNSET:
            field_dict["voice_seconds"] = voice_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        date = d.pop("date")

        audio_seconds = d.pop("audio_seconds", UNSET)

        completion_tokens = d.pop("completion_tokens", UNSET)

        input_characters = d.pop("input_characters", UNSET)

        prompt_tokens = d.pop("prompt_tokens", UNSET)

        request_duration_ms = d.pop("request_duration_ms", UNSET)

        total_tokens = d.pop("total_tokens", UNSET)

        voice_seconds = d.pop("voice_seconds", UNSET)

        usage_daily_entry = cls(
            count=count,
            date=date,
            audio_seconds=audio_seconds,
            completion_tokens=completion_tokens,
            input_characters=input_characters,
            prompt_tokens=prompt_tokens,
            request_duration_ms=request_duration_ms,
            total_tokens=total_tokens,
            voice_seconds=voice_seconds,
        )

        usage_daily_entry.additional_properties = d
        return usage_daily_entry

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
