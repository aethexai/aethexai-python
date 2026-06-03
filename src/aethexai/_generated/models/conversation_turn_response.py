from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="ConversationTurnResponse")


@_attrs_define
class ConversationTurnResponse:
    """
    Attributes:
        id (str):
        role (str):
        turn_index (int):
        confidence (float | None | Unset):
        created_at (None | str | Unset):
        llm_latency_ms (int | None | Unset):
        stt_latency_ms (int | None | Unset):
        text (str | Unset):  Default: ''.
        tool_calls (list[Any] | None | Unset):
        total_latency_ms (int | None | Unset):
        tts_latency_ms (int | None | Unset):
    """

    id: str
    role: str
    turn_index: int
    confidence: float | None | Unset = UNSET
    created_at: None | str | Unset = UNSET
    llm_latency_ms: int | None | Unset = UNSET
    stt_latency_ms: int | None | Unset = UNSET
    text: str | Unset = ""
    tool_calls: list[Any] | None | Unset = UNSET
    total_latency_ms: int | None | Unset = UNSET
    tts_latency_ms: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        role = self.role

        turn_index = self.turn_index

        confidence: float | None | Unset
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        llm_latency_ms: int | None | Unset
        if isinstance(self.llm_latency_ms, Unset):
            llm_latency_ms = UNSET
        else:
            llm_latency_ms = self.llm_latency_ms

        stt_latency_ms: int | None | Unset
        if isinstance(self.stt_latency_ms, Unset):
            stt_latency_ms = UNSET
        else:
            stt_latency_ms = self.stt_latency_ms

        text = self.text

        tool_calls: list[Any] | None | Unset
        if isinstance(self.tool_calls, Unset):
            tool_calls = UNSET
        elif isinstance(self.tool_calls, list):
            tool_calls = self.tool_calls

        else:
            tool_calls = self.tool_calls

        total_latency_ms: int | None | Unset
        if isinstance(self.total_latency_ms, Unset):
            total_latency_ms = UNSET
        else:
            total_latency_ms = self.total_latency_ms

        tts_latency_ms: int | None | Unset
        if isinstance(self.tts_latency_ms, Unset):
            tts_latency_ms = UNSET
        else:
            tts_latency_ms = self.tts_latency_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "role": role,
                "turn_index": turn_index,
            }
        )
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if llm_latency_ms is not UNSET:
            field_dict["llm_latency_ms"] = llm_latency_ms
        if stt_latency_ms is not UNSET:
            field_dict["stt_latency_ms"] = stt_latency_ms
        if text is not UNSET:
            field_dict["text"] = text
        if tool_calls is not UNSET:
            field_dict["tool_calls"] = tool_calls
        if total_latency_ms is not UNSET:
            field_dict["total_latency_ms"] = total_latency_ms
        if tts_latency_ms is not UNSET:
            field_dict["tts_latency_ms"] = tts_latency_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        role = d.pop("role")

        turn_index = d.pop("turn_index")

        def _parse_confidence(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_llm_latency_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        llm_latency_ms = _parse_llm_latency_ms(d.pop("llm_latency_ms", UNSET))

        def _parse_stt_latency_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        stt_latency_ms = _parse_stt_latency_ms(d.pop("stt_latency_ms", UNSET))

        text = d.pop("text", UNSET)

        def _parse_tool_calls(data: object) -> list[Any] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tool_calls_type_0 = cast(list[Any], data)

                return tool_calls_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Any] | None | Unset, data)

        tool_calls = _parse_tool_calls(d.pop("tool_calls", UNSET))

        def _parse_total_latency_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_latency_ms = _parse_total_latency_ms(d.pop("total_latency_ms", UNSET))

        def _parse_tts_latency_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        tts_latency_ms = _parse_tts_latency_ms(d.pop("tts_latency_ms", UNSET))

        conversation_turn_response = cls(
            id=id,
            role=role,
            turn_index=turn_index,
            confidence=confidence,
            created_at=created_at,
            llm_latency_ms=llm_latency_ms,
            stt_latency_ms=stt_latency_ms,
            text=text,
            tool_calls=tool_calls,
            total_latency_ms=total_latency_ms,
            tts_latency_ms=tts_latency_ms,
        )

        conversation_turn_response.additional_properties = d
        return conversation_turn_response

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
