from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.conversation_diagnostic_event_response_metadata_type_0 import (
        ConversationDiagnosticEventResponseMetadataType0,
    )


T = TypeVar("T", bound="ConversationDiagnosticEventResponse")


@_attrs_define
class ConversationDiagnosticEventResponse:
    """
    Attributes:
        event_type (str):
        id (str):
        severity (str):
        call_sid (None | str | Unset):
        created_at (None | str | Unset):
        elapsed_ms (int | None | Unset):
        latency_ms (int | None | Unset):
        metadata (ConversationDiagnosticEventResponseMetadataType0 | None | Unset):
        outcome (None | str | Unset):
        reason (None | str | Unset):
        session_id (None | str | Unset):
        stage (None | str | Unset):
        transport (None | str | Unset):
        turn_index (int | None | Unset):
    """

    event_type: str
    id: str
    severity: str
    call_sid: None | str | Unset = UNSET
    created_at: None | str | Unset = UNSET
    elapsed_ms: int | None | Unset = UNSET
    latency_ms: int | None | Unset = UNSET
    metadata: ConversationDiagnosticEventResponseMetadataType0 | None | Unset = UNSET
    outcome: None | str | Unset = UNSET
    reason: None | str | Unset = UNSET
    session_id: None | str | Unset = UNSET
    stage: None | str | Unset = UNSET
    transport: None | str | Unset = UNSET
    turn_index: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.conversation_diagnostic_event_response_metadata_type_0 import (
            ConversationDiagnosticEventResponseMetadataType0,
        )

        event_type = self.event_type

        id = self.id

        severity = self.severity

        call_sid: None | str | Unset
        if isinstance(self.call_sid, Unset):
            call_sid = UNSET
        else:
            call_sid = self.call_sid

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        elapsed_ms: int | None | Unset
        if isinstance(self.elapsed_ms, Unset):
            elapsed_ms = UNSET
        else:
            elapsed_ms = self.elapsed_ms

        latency_ms: int | None | Unset
        if isinstance(self.latency_ms, Unset):
            latency_ms = UNSET
        else:
            latency_ms = self.latency_ms

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, ConversationDiagnosticEventResponseMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        outcome: None | str | Unset
        if isinstance(self.outcome, Unset):
            outcome = UNSET
        else:
            outcome = self.outcome

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        session_id: None | str | Unset
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        else:
            session_id = self.session_id

        stage: None | str | Unset
        if isinstance(self.stage, Unset):
            stage = UNSET
        else:
            stage = self.stage

        transport: None | str | Unset
        if isinstance(self.transport, Unset):
            transport = UNSET
        else:
            transport = self.transport

        turn_index: int | None | Unset
        if isinstance(self.turn_index, Unset):
            turn_index = UNSET
        else:
            turn_index = self.turn_index

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_type": event_type,
                "id": id,
                "severity": severity,
            }
        )
        if call_sid is not UNSET:
            field_dict["call_sid"] = call_sid
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if elapsed_ms is not UNSET:
            field_dict["elapsed_ms"] = elapsed_ms
        if latency_ms is not UNSET:
            field_dict["latency_ms"] = latency_ms
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if outcome is not UNSET:
            field_dict["outcome"] = outcome
        if reason is not UNSET:
            field_dict["reason"] = reason
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if stage is not UNSET:
            field_dict["stage"] = stage
        if transport is not UNSET:
            field_dict["transport"] = transport
        if turn_index is not UNSET:
            field_dict["turn_index"] = turn_index

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conversation_diagnostic_event_response_metadata_type_0 import (
            ConversationDiagnosticEventResponseMetadataType0,
        )

        d = dict(src_dict)
        event_type = d.pop("event_type")

        id = d.pop("id")

        severity = d.pop("severity")

        def _parse_call_sid(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        call_sid = _parse_call_sid(d.pop("call_sid", UNSET))

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_elapsed_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        elapsed_ms = _parse_elapsed_ms(d.pop("elapsed_ms", UNSET))

        def _parse_latency_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        latency_ms = _parse_latency_ms(d.pop("latency_ms", UNSET))

        def _parse_metadata(
            data: object,
        ) -> ConversationDiagnosticEventResponseMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ConversationDiagnosticEventResponseMetadataType0.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ConversationDiagnosticEventResponseMetadataType0 | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_outcome(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        outcome = _parse_outcome(d.pop("outcome", UNSET))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_stage(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        stage = _parse_stage(d.pop("stage", UNSET))

        def _parse_transport(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        transport = _parse_transport(d.pop("transport", UNSET))

        def _parse_turn_index(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        turn_index = _parse_turn_index(d.pop("turn_index", UNSET))

        conversation_diagnostic_event_response = cls(
            event_type=event_type,
            id=id,
            severity=severity,
            call_sid=call_sid,
            created_at=created_at,
            elapsed_ms=elapsed_ms,
            latency_ms=latency_ms,
            metadata=metadata,
            outcome=outcome,
            reason=reason,
            session_id=session_id,
            stage=stage,
            transport=transport,
            turn_index=turn_index,
        )

        conversation_diagnostic_event_response.additional_properties = d
        return conversation_diagnostic_event_response

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
