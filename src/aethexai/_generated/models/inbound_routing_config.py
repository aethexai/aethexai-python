from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.inbound_routing_config_fallback_action import InboundRoutingConfigFallbackAction
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="InboundRoutingConfig")


@_attrs_define
class InboundRoutingConfig:
    """
    Attributes:
        fallback_action (InboundRoutingConfigFallbackAction | Unset):  Default:
            InboundRoutingConfigFallbackAction.HANGUP.
        fallback_number (None | str | Unset):
        max_ring_seconds (int | Unset):  Default: 30.
    """

    fallback_action: InboundRoutingConfigFallbackAction | Unset = (
        InboundRoutingConfigFallbackAction.HANGUP
    )
    fallback_number: None | str | Unset = UNSET
    max_ring_seconds: int | Unset = 30
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fallback_action: str | Unset = UNSET
        if not isinstance(self.fallback_action, Unset):
            fallback_action = self.fallback_action.value

        fallback_number: None | str | Unset
        if isinstance(self.fallback_number, Unset):
            fallback_number = UNSET
        else:
            fallback_number = self.fallback_number

        max_ring_seconds = self.max_ring_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fallback_action is not UNSET:
            field_dict["fallback_action"] = fallback_action
        if fallback_number is not UNSET:
            field_dict["fallback_number"] = fallback_number
        if max_ring_seconds is not UNSET:
            field_dict["max_ring_seconds"] = max_ring_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _fallback_action = d.pop("fallback_action", UNSET)
        fallback_action: InboundRoutingConfigFallbackAction | Unset
        if isinstance(_fallback_action, Unset):
            fallback_action = UNSET
        else:
            fallback_action = InboundRoutingConfigFallbackAction(_fallback_action)

        def _parse_fallback_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fallback_number = _parse_fallback_number(d.pop("fallback_number", UNSET))

        max_ring_seconds = d.pop("max_ring_seconds", UNSET)

        inbound_routing_config = cls(
            fallback_action=fallback_action,
            fallback_number=fallback_number,
            max_ring_seconds=max_ring_seconds,
        )

        inbound_routing_config.additional_properties = d
        return inbound_routing_config

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
