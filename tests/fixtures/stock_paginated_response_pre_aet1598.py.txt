from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="PaginatedResponse")


@_attrs_define
class PaginatedResponse:
    """
    Attributes:
        data (list[Any] | Unset):
        limit (int | Unset):  Default: 50.
        offset (int | Unset):  Default: 0.
        total (int | Unset):  Default: 0.
    """

    data: list[Any] | Unset = UNSET
    limit: int | Unset = 50
    offset: int | Unset = 0
    total: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: list[Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data

        limit = self.limit

        offset = self.offset

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if limit is not UNSET:
            field_dict["limit"] = limit
        if offset is not UNSET:
            field_dict["offset"] = offset
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data = cast(list[Any], d.pop("data", UNSET))

        limit = d.pop("limit", UNSET)

        offset = d.pop("offset", UNSET)

        total = d.pop("total", UNSET)

        paginated_response = cls(
            data=data,
            limit=limit,
            offset=offset,
            total=total,
        )

        paginated_response.additional_properties = d
        return paginated_response

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
