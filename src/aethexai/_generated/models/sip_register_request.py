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


T = TypeVar("T", bound="SipRegisterRequest")


@_attrs_define
class SipRegisterRequest:
    """
    Attributes:
        phone_number (str):
        trunk_id (str):
        agent_id (None | str | Unset):
        friendly_name (str | Unset):  Default: ''.
        inbound (InboundRoutingConfig | None | Unset):
        outbound_enabled (bool | Unset):  Default: False.
    """

    phone_number: str
    trunk_id: str
    agent_id: None | str | Unset = UNSET
    friendly_name: str | Unset = ""
    inbound: InboundRoutingConfig | None | Unset = UNSET
    outbound_enabled: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        from ..models.inbound_routing_config import InboundRoutingConfig

        phone_number = self.phone_number

        trunk_id = self.trunk_id

        agent_id: None | str | Unset
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        else:
            agent_id = self.agent_id

        friendly_name = self.friendly_name

        inbound: dict[str, Any] | None | Unset
        if isinstance(self.inbound, Unset):
            inbound = UNSET
        elif isinstance(self.inbound, InboundRoutingConfig):
            inbound = self.inbound.to_dict()
        else:
            inbound = self.inbound

        outbound_enabled = self.outbound_enabled

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "phone_number": phone_number,
                "trunk_id": trunk_id,
            }
        )
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if friendly_name is not UNSET:
            field_dict["friendly_name"] = friendly_name
        if inbound is not UNSET:
            field_dict["inbound"] = inbound
        if outbound_enabled is not UNSET:
            field_dict["outbound_enabled"] = outbound_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inbound_routing_config import InboundRoutingConfig

        d = dict(src_dict)
        phone_number = d.pop("phone_number")

        trunk_id = d.pop("trunk_id")

        def _parse_agent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_id = _parse_agent_id(d.pop("agent_id", UNSET))

        friendly_name = d.pop("friendly_name", UNSET)

        def _parse_inbound(data: object) -> InboundRoutingConfig | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                inbound_type_0 = InboundRoutingConfig.from_dict(data)

                return inbound_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(InboundRoutingConfig | None | Unset, data)

        inbound = _parse_inbound(d.pop("inbound", UNSET))

        outbound_enabled = d.pop("outbound_enabled", UNSET)

        sip_register_request = cls(
            phone_number=phone_number,
            trunk_id=trunk_id,
            agent_id=agent_id,
            friendly_name=friendly_name,
            inbound=inbound,
            outbound_enabled=outbound_enabled,
        )

        return sip_register_request
