from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.model_entry_provider import ModelEntryProvider


T = TypeVar("T", bound="ModelEntry")


@_attrs_define
class ModelEntry:
    """One row of the public LLM catalog.

    ``available`` reflects whether the deployment has the upstream API key
    needed to route this model. The default catalog filters unavailable
    entries so SDK pickers don't advertise something that will silently fall
    through to local vLLM at call time. Pass ``?include_unavailable=true``
    to see every public name the platform knows about, regardless of
    deployment configuration.

        Attributes:
            available (bool):
            id (str):
            provider (ModelEntryProvider):
    """

    available: bool
    id: str
    provider: ModelEntryProvider
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available = self.available

        id = self.id

        provider = self.provider.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available": available,
                "id": id,
                "provider": provider,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        available = d.pop("available")

        id = d.pop("id")

        provider = ModelEntryProvider(d.pop("provider"))

        model_entry = cls(
            available=available,
            id=id,
            provider=provider,
        )

        model_entry.additional_properties = d
        return model_entry

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
