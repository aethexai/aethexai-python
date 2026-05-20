from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.call_create_metadata import CallCreateMetadata


T = TypeVar("T", bound="CallCreate")


@_attrs_define
class CallCreate:
    """
    Attributes:
        agent_id (str):
        to_number (str):
        from_number (None | str | Unset):
        metadata (CallCreateMetadata | Unset):
    """

    agent_id: str
    to_number: str
    from_number: None | str | Unset = UNSET
    metadata: CallCreateMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.call_create_metadata import CallCreateMetadata

        agent_id = self.agent_id

        to_number = self.to_number

        from_number: None | str | Unset
        if isinstance(self.from_number, Unset):
            from_number = UNSET
        else:
            from_number = self.from_number

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agent_id": agent_id,
                "to_number": to_number,
            }
        )
        if from_number is not UNSET:
            field_dict["from_number"] = from_number
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_create_metadata import CallCreateMetadata

        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        to_number = d.pop("to_number")

        def _parse_from_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        from_number = _parse_from_number(d.pop("from_number", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: CallCreateMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CallCreateMetadata.from_dict(_metadata)

        call_create = cls(
            agent_id=agent_id,
            to_number=to_number,
            from_number=from_number,
            metadata=metadata,
        )

        call_create.additional_properties = d
        return call_create

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
