from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="ConversationResponse")


@_attrs_define
class ConversationResponse:
    """
    Attributes:
        id (str):
        agent_id (None | str | Unset):
        call_id (None | str | Unset):
        created_at (None | str | Unset):
        has_recording (bool | Unset):  Default: False.
        has_transcript (bool | Unset):  Default: False.
        recording_url (None | str | Unset):
        status (str | Unset):  Default: 'active'.
        total_duration_ms (int | None | Unset):
        transcript_text (None | str | Unset):
        turn_count (int | Unset):  Default: 0.
    """

    id: str
    agent_id: None | str | Unset = UNSET
    call_id: None | str | Unset = UNSET
    created_at: None | str | Unset = UNSET
    has_recording: bool | Unset = False
    has_transcript: bool | Unset = False
    recording_url: None | str | Unset = UNSET
    status: str | Unset = "active"
    total_duration_ms: int | None | Unset = UNSET
    transcript_text: None | str | Unset = UNSET
    turn_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        agent_id: None | str | Unset
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        else:
            agent_id = self.agent_id

        call_id: None | str | Unset
        if isinstance(self.call_id, Unset):
            call_id = UNSET
        else:
            call_id = self.call_id

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        has_recording = self.has_recording

        has_transcript = self.has_transcript

        recording_url: None | str | Unset
        if isinstance(self.recording_url, Unset):
            recording_url = UNSET
        else:
            recording_url = self.recording_url

        status = self.status

        total_duration_ms: int | None | Unset
        if isinstance(self.total_duration_ms, Unset):
            total_duration_ms = UNSET
        else:
            total_duration_ms = self.total_duration_ms

        transcript_text: None | str | Unset
        if isinstance(self.transcript_text, Unset):
            transcript_text = UNSET
        else:
            transcript_text = self.transcript_text

        turn_count = self.turn_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if call_id is not UNSET:
            field_dict["call_id"] = call_id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if has_recording is not UNSET:
            field_dict["has_recording"] = has_recording
        if has_transcript is not UNSET:
            field_dict["has_transcript"] = has_transcript
        if recording_url is not UNSET:
            field_dict["recording_url"] = recording_url
        if status is not UNSET:
            field_dict["status"] = status
        if total_duration_ms is not UNSET:
            field_dict["total_duration_ms"] = total_duration_ms
        if transcript_text is not UNSET:
            field_dict["transcript_text"] = transcript_text
        if turn_count is not UNSET:
            field_dict["turn_count"] = turn_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_agent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_id = _parse_agent_id(d.pop("agent_id", UNSET))

        def _parse_call_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        call_id = _parse_call_id(d.pop("call_id", UNSET))

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        has_recording = d.pop("has_recording", UNSET)

        has_transcript = d.pop("has_transcript", UNSET)

        def _parse_recording_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recording_url = _parse_recording_url(d.pop("recording_url", UNSET))

        status = d.pop("status", UNSET)

        def _parse_total_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_duration_ms = _parse_total_duration_ms(d.pop("total_duration_ms", UNSET))

        def _parse_transcript_text(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        transcript_text = _parse_transcript_text(d.pop("transcript_text", UNSET))

        turn_count = d.pop("turn_count", UNSET)

        conversation_response = cls(
            id=id,
            agent_id=agent_id,
            call_id=call_id,
            created_at=created_at,
            has_recording=has_recording,
            has_transcript=has_transcript,
            recording_url=recording_url,
            status=status,
            total_duration_ms=total_duration_ms,
            transcript_text=transcript_text,
            turn_count=turn_count,
        )

        conversation_response.additional_properties = d
        return conversation_response

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
