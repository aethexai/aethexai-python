from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="BatchCallResponse")


@_attrs_define
class BatchCallResponse:
    """
    Attributes:
        agent_id (str):
        batch_id (str):
        completed (int):
        failed (int):
        status (str):
        total (int):
        created_at (None | str | Unset):
        description (str | Unset):  Default: ''.
        end_at (None | str | Unset):
        name (None | str | Unset):
        start_at (None | str | Unset):
        updated_at (None | str | Unset):
    """

    agent_id: str
    batch_id: str
    completed: int
    failed: int
    status: str
    total: int
    created_at: None | str | Unset = UNSET
    description: str | Unset = ""
    end_at: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    start_at: None | str | Unset = UNSET
    updated_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        batch_id = self.batch_id

        completed = self.completed

        failed = self.failed

        status = self.status

        total = self.total

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        description = self.description

        end_at: None | str | Unset
        if isinstance(self.end_at, Unset):
            end_at = UNSET
        else:
            end_at = self.end_at

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        start_at: None | str | Unset
        if isinstance(self.start_at, Unset):
            start_at = UNSET
        else:
            start_at = self.start_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agent_id": agent_id,
                "batch_id": batch_id,
                "completed": completed,
                "failed": failed,
                "status": status,
                "total": total,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if description is not UNSET:
            field_dict["description"] = description
        if end_at is not UNSET:
            field_dict["end_at"] = end_at
        if name is not UNSET:
            field_dict["name"] = name
        if start_at is not UNSET:
            field_dict["start_at"] = start_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        batch_id = d.pop("batch_id")

        completed = d.pop("completed")

        failed = d.pop("failed")

        status = d.pop("status")

        total = d.pop("total")

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        description = d.pop("description", UNSET)

        def _parse_end_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        end_at = _parse_end_at(d.pop("end_at", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_start_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        start_at = _parse_start_at(d.pop("start_at", UNSET))

        def _parse_updated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        batch_call_response = cls(
            agent_id=agent_id,
            batch_id=batch_id,
            completed=completed,
            failed=failed,
            status=status,
            total=total,
            created_at=created_at,
            description=description,
            end_at=end_at,
            name=name,
            start_at=start_at,
            updated_at=updated_at,
        )

        batch_call_response.additional_properties = d
        return batch_call_response

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
