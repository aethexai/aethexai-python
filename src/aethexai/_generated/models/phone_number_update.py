from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.inbound_routing_config import InboundRoutingConfig


T = TypeVar("T", bound="PhoneNumberUpdate")


@_attrs_define
class PhoneNumberUpdate:
    """
    Attributes:
        agent_id (None | str | Unset):
        friendly_name (None | str | Unset):
        outbound_enabled (bool | None | Unset):
        routing_rules (InboundRoutingConfig | None | Unset):
    """

    agent_id: None | str | Unset = UNSET
    friendly_name: None | str | Unset = UNSET
    outbound_enabled: bool | None | Unset = UNSET
    routing_rules: InboundRoutingConfig | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.inbound_routing_config import InboundRoutingConfig

        agent_id: None | str | Unset
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        else:
            agent_id = self.agent_id

        friendly_name: None | str | Unset
        if isinstance(self.friendly_name, Unset):
            friendly_name = UNSET
        else:
            friendly_name = self.friendly_name

        outbound_enabled: bool | None | Unset
        if isinstance(self.outbound_enabled, Unset):
            outbound_enabled = UNSET
        else:
            outbound_enabled = self.outbound_enabled

        routing_rules: dict[str, Any] | None | Unset
        if isinstance(self.routing_rules, Unset):
            routing_rules = UNSET
        elif isinstance(self.routing_rules, InboundRoutingConfig):
            routing_rules = self.routing_rules.to_dict()
        else:
            routing_rules = self.routing_rules

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if friendly_name is not UNSET:
            field_dict["friendly_name"] = friendly_name
        if outbound_enabled is not UNSET:
            field_dict["outbound_enabled"] = outbound_enabled
        if routing_rules is not UNSET:
            field_dict["routing_rules"] = routing_rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inbound_routing_config import InboundRoutingConfig

        d = dict(src_dict)

        def _parse_agent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_id = _parse_agent_id(d.pop("agent_id", UNSET))

        def _parse_friendly_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        friendly_name = _parse_friendly_name(d.pop("friendly_name", UNSET))

        def _parse_outbound_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        outbound_enabled = _parse_outbound_enabled(d.pop("outbound_enabled", UNSET))

        def _parse_routing_rules(data: object) -> InboundRoutingConfig | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                routing_rules_type_0 = InboundRoutingConfig.from_dict(data)

                return routing_rules_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(InboundRoutingConfig | None | Unset, data)

        routing_rules = _parse_routing_rules(d.pop("routing_rules", UNSET))

        phone_number_update = cls(
            agent_id=agent_id,
            friendly_name=friendly_name,
            outbound_enabled=outbound_enabled,
            routing_rules=routing_rules,
        )

        phone_number_update.additional_properties = d
        return phone_number_update

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
