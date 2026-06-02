from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any, Generic, TypeVar, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="PaginatedResponse")  # type: ignore[type-arg]

_ItemT = TypeVar("_ItemT")


@_attrs_define
class PaginatedResponse(Generic[_ItemT]):
    """Single-page result from a list endpoint.

    **Important:** ``.data`` holds ONE page of results (default limit=50).
    It does NOT represent the full dataset. To page through all results,
    advance ``offset`` by ``limit`` while ``.has_more`` is ``True``::

        offset = 0
        limit = 50
        while True:
            page = client.list_agents(offset=offset, limit=limit)
            for agent in page.data:
                process(agent)
            if not page.has_more:
                break
            offset += limit

    Attributes:
        data (list[_ItemT] | Unset): Items on this page only.
        limit (int | Unset):  Default: 50.
        offset (int | Unset):  Default: 0.
        total (int | Unset):  Default: 0.
    """

    data: list[_ItemT] | Unset = UNSET
    limit: int | Unset = 50
    offset: int | Unset = 0
    total: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: list[_ItemT] | Unset = UNSET
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


    @property
    def has_more(self) -> bool:
        """``True`` when there are more pages beyond this one.

        Returns ``False`` when ``offset``, ``total``, or ``data`` are
        ``Unset``/``None`` (treat unknown pagination state as complete).
        """
        if isinstance(self.offset, Unset) or self.offset is None:
            return False
        if isinstance(self.total, Unset) or self.total is None:
            return False
        if isinstance(self.data, Unset) or self.data is None:
            return False
        return self.offset + len(self.data) < self.total

    def __getitem__(self, key: int | slice | str) -> Any:
        if isinstance(key, str):
            return self.additional_properties[key]
        if isinstance(self.data, Unset) or self.data is None:
            raise IndexError(key)
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: int | slice) -> None:
        if isinstance(self.data, Unset) or self.data is None:
            raise IndexError(key)
        del self.data[key]

    def __contains__(self, item: object) -> bool:
        if isinstance(self.data, Unset) or self.data is None:
            return False
        return item in self.data

    def __len__(self) -> int:
        if isinstance(self.data, Unset) or self.data is None:
            return 0
        return len(self.data)

    def __iter__(self) -> Iterator[_ItemT]:
        """Iterate the items on this page (e.g. ``for a in client.list_agents()``).

        Yields items from the CURRENT page only; loop while ``.has_more`` to
        consume every page.
        """
        if isinstance(self.data, Unset) or self.data is None:
            return iter(())
        return iter(self.data)
