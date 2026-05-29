from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="UsageByResourceEntry")


@_attrs_define
class UsageByResourceEntry:
    """One bucket value in ``UsageSummary.by_resource_type``. Keys mirror what the usage tracker aggregates per
    ``resource_type``:
    request count, token totals, audio seconds, and TTS input
    characters. All fields default to zero so an empty bucket is a
    well-typed object rather than a partial dict.

        Attributes:
            audio_seconds (float | Unset):  Default: 0.0.
            completion_tokens (int | Unset):  Default: 0.
            count (int | Unset):  Default: 0.
            input_characters (int | Unset):  Default: 0.
            prompt_tokens (int | Unset):  Default: 0.
            total_tokens (int | Unset):  Default: 0.
    """

    audio_seconds: float | Unset = 0.0
    completion_tokens: int | Unset = 0
    count: int | Unset = 0
    input_characters: int | Unset = 0
    prompt_tokens: int | Unset = 0
    total_tokens: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        audio_seconds = self.audio_seconds

        completion_tokens = self.completion_tokens

        count = self.count

        input_characters = self.input_characters

        prompt_tokens = self.prompt_tokens

        total_tokens = self.total_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if audio_seconds is not UNSET:
            field_dict["audio_seconds"] = audio_seconds
        if completion_tokens is not UNSET:
            field_dict["completion_tokens"] = completion_tokens
        if count is not UNSET:
            field_dict["count"] = count
        if input_characters is not UNSET:
            field_dict["input_characters"] = input_characters
        if prompt_tokens is not UNSET:
            field_dict["prompt_tokens"] = prompt_tokens
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        audio_seconds = d.pop("audio_seconds", UNSET)

        completion_tokens = d.pop("completion_tokens", UNSET)

        count = d.pop("count", UNSET)

        input_characters = d.pop("input_characters", UNSET)

        prompt_tokens = d.pop("prompt_tokens", UNSET)

        total_tokens = d.pop("total_tokens", UNSET)

        usage_by_resource_entry = cls(
            audio_seconds=audio_seconds,
            completion_tokens=completion_tokens,
            count=count,
            input_characters=input_characters,
            prompt_tokens=prompt_tokens,
            total_tokens=total_tokens,
        )

        usage_by_resource_entry.additional_properties = d
        return usage_by_resource_entry

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
