from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.call_response_direction import CallResponseDirection
from ..models.call_response_provider import CallResponseProvider
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.call_response_metadata import CallResponseMetadata


T = TypeVar("T", bound="CallResponse")


@_attrs_define
class CallResponse:
    """
    Attributes:
        id (str):
        agent_id (None | str | Unset):
        call_sid (None | str | Unset):
        conversation_id (None | str | Unset):
        cost_cents (int | None | Unset):
        created_at (None | str | Unset):
        direction (CallResponseDirection | Unset):  Default: CallResponseDirection.OUTBOUND.
        duration_seconds (float | None | Unset):
        from_number (None | str | Unset):
        initiated_via (str | Unset):  Default: 'api'.
        metadata (CallResponseMetadata | Unset):
        provider (CallResponseProvider | Unset):  Default: CallResponseProvider.TWILIO.
        status (str | Unset):  Default: 'queued'.
        to_number (None | str | Unset):
        updated_at (None | str | Unset):
        voice_session_id (None | str | Unset):
    """

    id: str
    agent_id: None | str | Unset = UNSET
    call_sid: None | str | Unset = UNSET
    conversation_id: None | str | Unset = UNSET
    cost_cents: int | None | Unset = UNSET
    created_at: None | str | Unset = UNSET
    direction: CallResponseDirection | Unset = CallResponseDirection.OUTBOUND
    duration_seconds: float | None | Unset = UNSET
    from_number: None | str | Unset = UNSET
    initiated_via: str | Unset = "api"
    metadata: CallResponseMetadata | Unset = UNSET
    provider: CallResponseProvider | Unset = CallResponseProvider.TWILIO
    status: str | Unset = "queued"
    to_number: None | str | Unset = UNSET
    updated_at: None | str | Unset = UNSET
    voice_session_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.call_response_metadata import CallResponseMetadata

        id = self.id

        agent_id: None | str | Unset
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        else:
            agent_id = self.agent_id

        call_sid: None | str | Unset
        if isinstance(self.call_sid, Unset):
            call_sid = UNSET
        else:
            call_sid = self.call_sid

        conversation_id: None | str | Unset
        if isinstance(self.conversation_id, Unset):
            conversation_id = UNSET
        else:
            conversation_id = self.conversation_id

        cost_cents: int | None | Unset
        if isinstance(self.cost_cents, Unset):
            cost_cents = UNSET
        else:
            cost_cents = self.cost_cents

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        direction: str | Unset = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        duration_seconds: float | None | Unset
        if isinstance(self.duration_seconds, Unset):
            duration_seconds = UNSET
        else:
            duration_seconds = self.duration_seconds

        from_number: None | str | Unset
        if isinstance(self.from_number, Unset):
            from_number = UNSET
        else:
            from_number = self.from_number

        initiated_via = self.initiated_via

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        provider: str | Unset = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.value

        status = self.status

        to_number: None | str | Unset
        if isinstance(self.to_number, Unset):
            to_number = UNSET
        else:
            to_number = self.to_number

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = self.updated_at

        voice_session_id: None | str | Unset
        if isinstance(self.voice_session_id, Unset):
            voice_session_id = UNSET
        else:
            voice_session_id = self.voice_session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if call_sid is not UNSET:
            field_dict["call_sid"] = call_sid
        if conversation_id is not UNSET:
            field_dict["conversation_id"] = conversation_id
        if cost_cents is not UNSET:
            field_dict["cost_cents"] = cost_cents
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if direction is not UNSET:
            field_dict["direction"] = direction
        if duration_seconds is not UNSET:
            field_dict["duration_seconds"] = duration_seconds
        if from_number is not UNSET:
            field_dict["from_number"] = from_number
        if initiated_via is not UNSET:
            field_dict["initiated_via"] = initiated_via
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if provider is not UNSET:
            field_dict["provider"] = provider
        if status is not UNSET:
            field_dict["status"] = status
        if to_number is not UNSET:
            field_dict["to_number"] = to_number
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if voice_session_id is not UNSET:
            field_dict["voice_session_id"] = voice_session_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_response_metadata import CallResponseMetadata

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_agent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_id = _parse_agent_id(d.pop("agent_id", UNSET))

        def _parse_call_sid(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        call_sid = _parse_call_sid(d.pop("call_sid", UNSET))

        def _parse_conversation_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        conversation_id = _parse_conversation_id(d.pop("conversation_id", UNSET))

        def _parse_cost_cents(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cost_cents = _parse_cost_cents(d.pop("cost_cents", UNSET))

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        _direction = d.pop("direction", UNSET)
        direction: CallResponseDirection | Unset
        if isinstance(_direction, Unset):
            direction = UNSET
        else:
            direction = CallResponseDirection(_direction)

        def _parse_duration_seconds(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        duration_seconds = _parse_duration_seconds(d.pop("duration_seconds", UNSET))

        def _parse_from_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        from_number = _parse_from_number(d.pop("from_number", UNSET))

        initiated_via = d.pop("initiated_via", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: CallResponseMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CallResponseMetadata.from_dict(_metadata)

        _provider = d.pop("provider", UNSET)
        provider: CallResponseProvider | Unset
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = CallResponseProvider(_provider)

        status = d.pop("status", UNSET)

        def _parse_to_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        to_number = _parse_to_number(d.pop("to_number", UNSET))

        def _parse_updated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_voice_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        voice_session_id = _parse_voice_session_id(d.pop("voice_session_id", UNSET))

        call_response = cls(
            id=id,
            agent_id=agent_id,
            call_sid=call_sid,
            conversation_id=conversation_id,
            cost_cents=cost_cents,
            created_at=created_at,
            direction=direction,
            duration_seconds=duration_seconds,
            from_number=from_number,
            initiated_via=initiated_via,
            metadata=metadata,
            provider=provider,
            status=status,
            to_number=to_number,
            updated_at=updated_at,
            voice_session_id=voice_session_id,
        )

        call_response.additional_properties = d
        return call_response

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
