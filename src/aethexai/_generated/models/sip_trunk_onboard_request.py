from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sip_trunk_onboard_request_auth_mode import SipTrunkOnboardRequestAuthMode
from ..models.sip_trunk_onboard_request_media_encryption import (
    SipTrunkOnboardRequestMediaEncryption,
)
from ..models.sip_trunk_onboard_request_transport import SipTrunkOnboardRequestTransport
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
    from ..models.destination_allowlist import DestinationAllowlist
    from ..models.inbound_routing_config import InboundRoutingConfig


T = TypeVar("T", bound="SipTrunkOnboardRequest")


@_attrs_define
class SipTrunkOnboardRequest:
    """One-shot BYO SIP trunk onboarding payload.

    Attributes:
        name (str):
        numbers (list[str]):
        outbound_address (str):
        agent_id (None | Unset | UUID):
        auth_mode (SipTrunkOnboardRequestAuthMode | Unset): Outbound trunk auth contract: digest credentials, provider-
            side IP ACL, or both. Default: SipTrunkOnboardRequestAuthMode.DIGEST.
        auth_password (None | str | Unset):
        auth_username (None | str | Unset):
        calls_per_hour_limit (int | Unset):  Default: 1000.
        destination_allowlist (DestinationAllowlist | Unset): Per-trunk outbound dialing guard. Enforced before every
            SIP INVITE.
        inbound (InboundRoutingConfig | None | Unset):
        max_concurrent_calls (int | Unset):  Default: 10.
        media_encryption (SipTrunkOnboardRequestMediaEncryption | Unset):  Default:
            SipTrunkOnboardRequestMediaEncryption.ALLOW.
        outbound_enabled (bool | Unset):  Default: True.
        set_as_tenant_default (bool | Unset):  Default: False.
        transport (SipTrunkOnboardRequestTransport | Unset):  Default: SipTrunkOnboardRequestTransport.UDP.
    """

    name: str
    numbers: list[str]
    outbound_address: str
    agent_id: None | Unset | UUID = UNSET
    auth_mode: SipTrunkOnboardRequestAuthMode | Unset = SipTrunkOnboardRequestAuthMode.DIGEST
    auth_password: None | str | Unset = UNSET
    auth_username: None | str | Unset = UNSET
    calls_per_hour_limit: int | Unset = 1000
    destination_allowlist: DestinationAllowlist | Unset = UNSET
    inbound: InboundRoutingConfig | None | Unset = UNSET
    max_concurrent_calls: int | Unset = 10
    media_encryption: SipTrunkOnboardRequestMediaEncryption | Unset = (
        SipTrunkOnboardRequestMediaEncryption.ALLOW
    )
    outbound_enabled: bool | Unset = True
    set_as_tenant_default: bool | Unset = False
    transport: SipTrunkOnboardRequestTransport | Unset = SipTrunkOnboardRequestTransport.UDP

    def to_dict(self) -> dict[str, Any]:
        from ..models.destination_allowlist import DestinationAllowlist
        from ..models.inbound_routing_config import InboundRoutingConfig

        name = self.name

        numbers = self.numbers

        outbound_address = self.outbound_address

        agent_id: None | str | Unset
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        elif isinstance(self.agent_id, UUID):
            agent_id = str(self.agent_id)
        else:
            agent_id = self.agent_id

        auth_mode: str | Unset = UNSET
        if not isinstance(self.auth_mode, Unset):
            auth_mode = self.auth_mode.value

        auth_password: None | str | Unset
        if isinstance(self.auth_password, Unset):
            auth_password = UNSET
        else:
            auth_password = self.auth_password

        auth_username: None | str | Unset
        if isinstance(self.auth_username, Unset):
            auth_username = UNSET
        else:
            auth_username = self.auth_username

        calls_per_hour_limit = self.calls_per_hour_limit

        destination_allowlist: dict[str, Any] | Unset = UNSET
        if not isinstance(self.destination_allowlist, Unset):
            destination_allowlist = self.destination_allowlist.to_dict()

        inbound: dict[str, Any] | None | Unset
        if isinstance(self.inbound, Unset):
            inbound = UNSET
        elif isinstance(self.inbound, InboundRoutingConfig):
            inbound = self.inbound.to_dict()
        else:
            inbound = self.inbound

        max_concurrent_calls = self.max_concurrent_calls

        media_encryption: str | Unset = UNSET
        if not isinstance(self.media_encryption, Unset):
            media_encryption = self.media_encryption.value

        outbound_enabled = self.outbound_enabled

        set_as_tenant_default = self.set_as_tenant_default

        transport: str | Unset = UNSET
        if not isinstance(self.transport, Unset):
            transport = self.transport.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "numbers": numbers,
                "outbound_address": outbound_address,
            }
        )
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if auth_mode is not UNSET:
            field_dict["auth_mode"] = auth_mode
        if auth_password is not UNSET:
            field_dict["auth_password"] = auth_password
        if auth_username is not UNSET:
            field_dict["auth_username"] = auth_username
        if calls_per_hour_limit is not UNSET:
            field_dict["calls_per_hour_limit"] = calls_per_hour_limit
        if destination_allowlist is not UNSET:
            field_dict["destination_allowlist"] = destination_allowlist
        if inbound is not UNSET:
            field_dict["inbound"] = inbound
        if max_concurrent_calls is not UNSET:
            field_dict["max_concurrent_calls"] = max_concurrent_calls
        if media_encryption is not UNSET:
            field_dict["media_encryption"] = media_encryption
        if outbound_enabled is not UNSET:
            field_dict["outbound_enabled"] = outbound_enabled
        if set_as_tenant_default is not UNSET:
            field_dict["set_as_tenant_default"] = set_as_tenant_default
        if transport is not UNSET:
            field_dict["transport"] = transport

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.destination_allowlist import DestinationAllowlist
        from ..models.inbound_routing_config import InboundRoutingConfig

        d = dict(src_dict)
        name = d.pop("name")

        numbers = cast(list[str], d.pop("numbers"))

        outbound_address = d.pop("outbound_address")

        def _parse_agent_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                agent_id_type_0 = UUID(data)

                return agent_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        agent_id = _parse_agent_id(d.pop("agent_id", UNSET))

        _auth_mode = d.pop("auth_mode", UNSET)
        auth_mode: SipTrunkOnboardRequestAuthMode | Unset
        if isinstance(_auth_mode, Unset):
            auth_mode = UNSET
        else:
            auth_mode = SipTrunkOnboardRequestAuthMode(_auth_mode)

        def _parse_auth_password(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        auth_password = _parse_auth_password(d.pop("auth_password", UNSET))

        def _parse_auth_username(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        auth_username = _parse_auth_username(d.pop("auth_username", UNSET))

        calls_per_hour_limit = d.pop("calls_per_hour_limit", UNSET)

        _destination_allowlist = d.pop("destination_allowlist", UNSET)
        destination_allowlist: DestinationAllowlist | Unset
        if isinstance(_destination_allowlist, Unset):
            destination_allowlist = UNSET
        else:
            destination_allowlist = DestinationAllowlist.from_dict(_destination_allowlist)

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

        max_concurrent_calls = d.pop("max_concurrent_calls", UNSET)

        _media_encryption = d.pop("media_encryption", UNSET)
        media_encryption: SipTrunkOnboardRequestMediaEncryption | Unset
        if isinstance(_media_encryption, Unset):
            media_encryption = UNSET
        else:
            media_encryption = SipTrunkOnboardRequestMediaEncryption(_media_encryption)

        outbound_enabled = d.pop("outbound_enabled", UNSET)

        set_as_tenant_default = d.pop("set_as_tenant_default", UNSET)

        _transport = d.pop("transport", UNSET)
        transport: SipTrunkOnboardRequestTransport | Unset
        if isinstance(_transport, Unset):
            transport = UNSET
        else:
            transport = SipTrunkOnboardRequestTransport(_transport)

        sip_trunk_onboard_request = cls(
            name=name,
            numbers=numbers,
            outbound_address=outbound_address,
            agent_id=agent_id,
            auth_mode=auth_mode,
            auth_password=auth_password,
            auth_username=auth_username,
            calls_per_hour_limit=calls_per_hour_limit,
            destination_allowlist=destination_allowlist,
            inbound=inbound,
            max_concurrent_calls=max_concurrent_calls,
            media_encryption=media_encryption,
            outbound_enabled=outbound_enabled,
            set_as_tenant_default=set_as_tenant_default,
            transport=transport,
        )

        return sip_trunk_onboard_request
