from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.call_record_create_direction import CallRecordCreateDirection
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.call_record_create_metadata import CallRecordCreateMetadata


T = TypeVar("T", bound="CallRecordCreate")


@_attrs_define
class CallRecordCreate:
    """
    Attributes:
        agent_id (str):
        direction (CallRecordCreateDirection | Unset):  Default: CallRecordCreateDirection.OUTBOUND.
        from_number (None | str | Unset):
        metadata (CallRecordCreateMetadata | Unset):
        to_number (None | str | Unset):
    """

    agent_id: str
    direction: CallRecordCreateDirection | Unset = CallRecordCreateDirection.OUTBOUND
    from_number: None | str | Unset = UNSET
    metadata: CallRecordCreateMetadata | Unset = UNSET
    to_number: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.call_record_create_metadata import CallRecordCreateMetadata

        agent_id = self.agent_id

        direction: str | Unset = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        from_number: None | str | Unset
        if isinstance(self.from_number, Unset):
            from_number = UNSET
        else:
            from_number = self.from_number

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        to_number: None | str | Unset
        if isinstance(self.to_number, Unset):
            to_number = UNSET
        else:
            to_number = self.to_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agent_id": agent_id,
            }
        )
        if direction is not UNSET:
            field_dict["direction"] = direction
        if from_number is not UNSET:
            field_dict["from_number"] = from_number
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if to_number is not UNSET:
            field_dict["to_number"] = to_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_record_create_metadata import CallRecordCreateMetadata

        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        _direction = d.pop("direction", UNSET)
        direction: CallRecordCreateDirection | Unset
        if isinstance(_direction, Unset):
            direction = UNSET
        else:
            direction = CallRecordCreateDirection(_direction)

        def _parse_from_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        from_number = _parse_from_number(d.pop("from_number", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: CallRecordCreateMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CallRecordCreateMetadata.from_dict(_metadata)

        def _parse_to_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        to_number = _parse_to_number(d.pop("to_number", UNSET))

        call_record_create = cls(
            agent_id=agent_id,
            direction=direction,
            from_number=from_number,
            metadata=metadata,
            to_number=to_number,
        )

        call_record_create.additional_properties = d
        return call_record_create

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
