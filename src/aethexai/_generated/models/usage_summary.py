from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.usage_summary_by_resource_type import UsageSummaryByResourceType


T = TypeVar("T", bound="UsageSummary")


@_attrs_define
class UsageSummary:
    """
    Attributes:
        by_resource_type (UsageSummaryByResourceType | Unset):
        total_api_requests (int | Unset):  Default: 0.
        total_audio_seconds (float | Unset): Sum of audio_seconds across ALL resource types: voice calls, transcription
            input audio, and any other rows that record an audio duration. For agent-active time alone, use
            total_voice_seconds. Default: 0.0.
        total_completion_tokens (int | Unset):  Default: 0.
        total_input_characters (int | Unset):  Default: 0.
        total_prompt_tokens (int | Unset):  Default: 0.
        total_request_duration_ms (int | Unset): Sum of HTTP request duration_ms across every non-voice REST endpoint
            under ``/api/v1/*``. Voice calls are not HTTP requests; see total_voice_seconds. Default: 0.
        total_tokens (int | Unset):  Default: 0.
        total_voice_seconds (float | Unset): Sum of audio_seconds across voice_call rows. This is the agent-active time
            captured by the voice pipeline at end-of-call. Default: 0.0.
    """

    by_resource_type: UsageSummaryByResourceType | Unset = UNSET
    total_api_requests: int | Unset = 0
    total_audio_seconds: float | Unset = 0.0
    total_completion_tokens: int | Unset = 0
    total_input_characters: int | Unset = 0
    total_prompt_tokens: int | Unset = 0
    total_request_duration_ms: int | Unset = 0
    total_tokens: int | Unset = 0
    total_voice_seconds: float | Unset = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_summary_by_resource_type import UsageSummaryByResourceType

        by_resource_type: dict[str, Any] | Unset = UNSET
        if not isinstance(self.by_resource_type, Unset):
            by_resource_type = self.by_resource_type.to_dict()

        total_api_requests = self.total_api_requests

        total_audio_seconds = self.total_audio_seconds

        total_completion_tokens = self.total_completion_tokens

        total_input_characters = self.total_input_characters

        total_prompt_tokens = self.total_prompt_tokens

        total_request_duration_ms = self.total_request_duration_ms

        total_tokens = self.total_tokens

        total_voice_seconds = self.total_voice_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if by_resource_type is not UNSET:
            field_dict["by_resource_type"] = by_resource_type
        if total_api_requests is not UNSET:
            field_dict["total_api_requests"] = total_api_requests
        if total_audio_seconds is not UNSET:
            field_dict["total_audio_seconds"] = total_audio_seconds
        if total_completion_tokens is not UNSET:
            field_dict["total_completion_tokens"] = total_completion_tokens
        if total_input_characters is not UNSET:
            field_dict["total_input_characters"] = total_input_characters
        if total_prompt_tokens is not UNSET:
            field_dict["total_prompt_tokens"] = total_prompt_tokens
        if total_request_duration_ms is not UNSET:
            field_dict["total_request_duration_ms"] = total_request_duration_ms
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens
        if total_voice_seconds is not UNSET:
            field_dict["total_voice_seconds"] = total_voice_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_summary_by_resource_type import UsageSummaryByResourceType

        d = dict(src_dict)
        _by_resource_type = d.pop("by_resource_type", UNSET)
        by_resource_type: UsageSummaryByResourceType | Unset
        if isinstance(_by_resource_type, Unset):
            by_resource_type = UNSET
        else:
            by_resource_type = UsageSummaryByResourceType.from_dict(_by_resource_type)

        total_api_requests = d.pop("total_api_requests", UNSET)

        total_audio_seconds = d.pop("total_audio_seconds", UNSET)

        total_completion_tokens = d.pop("total_completion_tokens", UNSET)

        total_input_characters = d.pop("total_input_characters", UNSET)

        total_prompt_tokens = d.pop("total_prompt_tokens", UNSET)

        total_request_duration_ms = d.pop("total_request_duration_ms", UNSET)

        total_tokens = d.pop("total_tokens", UNSET)

        total_voice_seconds = d.pop("total_voice_seconds", UNSET)

        usage_summary = cls(
            by_resource_type=by_resource_type,
            total_api_requests=total_api_requests,
            total_audio_seconds=total_audio_seconds,
            total_completion_tokens=total_completion_tokens,
            total_input_characters=total_input_characters,
            total_prompt_tokens=total_prompt_tokens,
            total_request_duration_ms=total_request_duration_ms,
            total_tokens=total_tokens,
            total_voice_seconds=total_voice_seconds,
        )

        usage_summary.additional_properties = d
        return usage_summary

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
