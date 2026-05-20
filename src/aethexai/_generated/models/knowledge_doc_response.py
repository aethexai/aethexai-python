from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="KnowledgeDocResponse")


@_attrs_define
class KnowledgeDocResponse:
    """
    Attributes:
        id (str):
        chunk_count (int | None | Unset):
        filename (str | Unset):  Default: ''.
        status (str | Unset):  Default: 'processing'.
    """

    id: str
    chunk_count: int | None | Unset = UNSET
    filename: str | Unset = ""
    status: str | Unset = "processing"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        chunk_count: int | None | Unset
        if isinstance(self.chunk_count, Unset):
            chunk_count = UNSET
        else:
            chunk_count = self.chunk_count

        filename = self.filename

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if chunk_count is not UNSET:
            field_dict["chunk_count"] = chunk_count
        if filename is not UNSET:
            field_dict["filename"] = filename
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_chunk_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        chunk_count = _parse_chunk_count(d.pop("chunk_count", UNSET))

        filename = d.pop("filename", UNSET)

        status = d.pop("status", UNSET)

        knowledge_doc_response = cls(
            id=id,
            chunk_count=chunk_count,
            filename=filename,
            status=status,
        )

        knowledge_doc_response.additional_properties = d
        return knowledge_doc_response

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
