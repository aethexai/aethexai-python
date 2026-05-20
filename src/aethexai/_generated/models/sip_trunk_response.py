from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sip_trunk_response_auth_mode import SipTrunkResponseAuthMode
from ..models.sip_trunk_response_media_encryption import SipTrunkResponseMediaEncryption
from ..models.sip_trunk_response_transport import SipTrunkResponseTransport
from ..models.sip_trunk_response_type import SipTrunkResponseType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.destination_allowlist import DestinationAllowlist


T = TypeVar("T", bound="SipTrunkResponse")


@_attrs_define
class SipTrunkResponse:
    """
    Attributes:
        allowed_addresses (list[str]):
        auth_mode (SipTrunkResponseAuthMode):
        auth_username (None | str):
        calls_per_hour_limit (int):
        created_at (None | str):
        destination_allowlist (DestinationAllowlist): Per-trunk outbound dialing guard. Enforced before every SIP
            INVITE.
        id (str):
        lk_trunk_id (str):
        max_concurrent_calls (int):
        media_encryption (SipTrunkResponseMediaEncryption):
        name (str):
        numbers (list[str]):
        outbound_address (None | str):
        status (str):
        transport (SipTrunkResponseTransport):
        type_ (SipTrunkResponseType):
        tenant_id (None | str | Unset):
    """

    allowed_addresses: list[str]
    auth_mode: SipTrunkResponseAuthMode
    auth_username: None | str
    calls_per_hour_limit: int
    created_at: None | str
    destination_allowlist: DestinationAllowlist
    id: str
    lk_trunk_id: str
    max_concurrent_calls: int
    media_encryption: SipTrunkResponseMediaEncryption
    name: str
    numbers: list[str]
    outbound_address: None | str
    status: str
    transport: SipTrunkResponseTransport
    type_: SipTrunkResponseType
    tenant_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.destination_allowlist import DestinationAllowlist

        allowed_addresses = self.allowed_addresses

        auth_mode = self.auth_mode.value

        auth_username: None | str
        auth_username = self.auth_username

        calls_per_hour_limit = self.calls_per_hour_limit

        created_at: None | str
        created_at = self.created_at

        destination_allowlist = self.destination_allowlist.to_dict()

        id = self.id

        lk_trunk_id = self.lk_trunk_id

        max_concurrent_calls = self.max_concurrent_calls

        media_encryption = self.media_encryption.value

        name = self.name

        numbers = self.numbers

        outbound_address: None | str
        outbound_address = self.outbound_address

        status = self.status

        transport = self.transport.value

        type_ = self.type_.value

        tenant_id: None | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        else:
            tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "allowed_addresses": allowed_addresses,
                "auth_mode": auth_mode,
                "auth_username": auth_username,
                "calls_per_hour_limit": calls_per_hour_limit,
                "created_at": created_at,
                "destination_allowlist": destination_allowlist,
                "id": id,
                "lk_trunk_id": lk_trunk_id,
                "max_concurrent_calls": max_concurrent_calls,
                "media_encryption": media_encryption,
                "name": name,
                "numbers": numbers,
                "outbound_address": outbound_address,
                "status": status,
                "transport": transport,
                "type": type_,
            }
        )
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.destination_allowlist import DestinationAllowlist

        d = dict(src_dict)
        allowed_addresses = cast(list[str], d.pop("allowed_addresses"))

        auth_mode = SipTrunkResponseAuthMode(d.pop("auth_mode"))

        def _parse_auth_username(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        auth_username = _parse_auth_username(d.pop("auth_username"))

        calls_per_hour_limit = d.pop("calls_per_hour_limit")

        def _parse_created_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        created_at = _parse_created_at(d.pop("created_at"))

        destination_allowlist = DestinationAllowlist.from_dict(d.pop("destination_allowlist"))

        id = d.pop("id")

        lk_trunk_id = d.pop("lk_trunk_id")

        max_concurrent_calls = d.pop("max_concurrent_calls")

        media_encryption = SipTrunkResponseMediaEncryption(d.pop("media_encryption"))

        name = d.pop("name")

        numbers = cast(list[str], d.pop("numbers"))

        def _parse_outbound_address(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        outbound_address = _parse_outbound_address(d.pop("outbound_address"))

        status = d.pop("status")

        transport = SipTrunkResponseTransport(d.pop("transport"))

        type_ = SipTrunkResponseType(d.pop("type"))

        def _parse_tenant_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tenant_id = _parse_tenant_id(d.pop("tenant_id", UNSET))

        sip_trunk_response = cls(
            allowed_addresses=allowed_addresses,
            auth_mode=auth_mode,
            auth_username=auth_username,
            calls_per_hour_limit=calls_per_hour_limit,
            created_at=created_at,
            destination_allowlist=destination_allowlist,
            id=id,
            lk_trunk_id=lk_trunk_id,
            max_concurrent_calls=max_concurrent_calls,
            media_encryption=media_encryption,
            name=name,
            numbers=numbers,
            outbound_address=outbound_address,
            status=status,
            transport=transport,
            type_=type_,
            tenant_id=tenant_id,
        )

        sip_trunk_response.additional_properties = d
        return sip_trunk_response

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
