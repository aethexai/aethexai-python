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


T = TypeVar("T", bound="PhoneNumberResponse")


@_attrs_define
class PhoneNumberResponse:
    """
    Attributes:
        id (str):
        phone_number (str):
        agent_id (None | str | Unset):
        created_at (None | str | Unset):
        friendly_name (str | Unset):  Default: ''.
        outbound_enabled (bool | Unset):  Default: False.
        provider (str | Unset):  Default: 'twilio'.
        routing_rules (InboundRoutingConfig | None | Unset):
        status (str | Unset):  Default: 'active'.
        trunk_id (None | str | Unset):
    """

    id: str
    phone_number: str
    agent_id: None | str | Unset = UNSET
    created_at: None | str | Unset = UNSET
    friendly_name: str | Unset = ""
    outbound_enabled: bool | Unset = False
    provider: str | Unset = "twilio"
    routing_rules: InboundRoutingConfig | None | Unset = UNSET
    status: str | Unset = "active"
    trunk_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.inbound_routing_config import InboundRoutingConfig

        id = self.id

        phone_number = self.phone_number

        agent_id: None | str | Unset
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        else:
            agent_id = self.agent_id

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        friendly_name = self.friendly_name

        outbound_enabled = self.outbound_enabled

        provider = self.provider

        routing_rules: dict[str, Any] | None | Unset
        if isinstance(self.routing_rules, Unset):
            routing_rules = UNSET
        elif isinstance(self.routing_rules, InboundRoutingConfig):
            routing_rules = self.routing_rules.to_dict()
        else:
            routing_rules = self.routing_rules

        status = self.status

        trunk_id: None | str | Unset
        if isinstance(self.trunk_id, Unset):
            trunk_id = UNSET
        else:
            trunk_id = self.trunk_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "phone_number": phone_number,
            }
        )
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if friendly_name is not UNSET:
            field_dict["friendly_name"] = friendly_name
        if outbound_enabled is not UNSET:
            field_dict["outbound_enabled"] = outbound_enabled
        if provider is not UNSET:
            field_dict["provider"] = provider
        if routing_rules is not UNSET:
            field_dict["routing_rules"] = routing_rules
        if status is not UNSET:
            field_dict["status"] = status
        if trunk_id is not UNSET:
            field_dict["trunk_id"] = trunk_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inbound_routing_config import InboundRoutingConfig

        d = dict(src_dict)
        id = d.pop("id")

        phone_number = d.pop("phone_number")

        def _parse_agent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_id = _parse_agent_id(d.pop("agent_id", UNSET))

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        friendly_name = d.pop("friendly_name", UNSET)

        outbound_enabled = d.pop("outbound_enabled", UNSET)

        provider = d.pop("provider", UNSET)

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

        status = d.pop("status", UNSET)

        def _parse_trunk_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trunk_id = _parse_trunk_id(d.pop("trunk_id", UNSET))

        phone_number_response = cls(
            id=id,
            phone_number=phone_number,
            agent_id=agent_id,
            created_at=created_at,
            friendly_name=friendly_name,
            outbound_enabled=outbound_enabled,
            provider=provider,
            routing_rules=routing_rules,
            status=status,
            trunk_id=trunk_id,
        )

        phone_number_response.additional_properties = d
        return phone_number_response

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
