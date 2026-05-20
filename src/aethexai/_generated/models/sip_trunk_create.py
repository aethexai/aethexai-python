from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sip_trunk_create_auth_mode import SipTrunkCreateAuthMode
from ..models.sip_trunk_create_media_encryption import SipTrunkCreateMediaEncryption
from ..models.sip_trunk_create_transport import SipTrunkCreateTransport
from ..models.sip_trunk_create_type import SipTrunkCreateType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.destination_allowlist import DestinationAllowlist


T = TypeVar("T", bound="SipTrunkCreate")


@_attrs_define
class SipTrunkCreate:
    """
    Attributes:
        name (str):
        type_ (SipTrunkCreateType):
        allowed_addresses (list[str] | Unset):
        auth_mode (SipTrunkCreateAuthMode | Unset): Outbound trunk auth contract: digest credentials, provider-side IP
            ACL, or both. Inbound trunks can also store this as metadata. Default: SipTrunkCreateAuthMode.DIGEST.
        auth_password (None | str | Unset):
        auth_username (None | str | Unset):
        calls_per_hour_limit (int | Unset):  Default: 1000.
        destination_allowlist (DestinationAllowlist | Unset): Per-trunk outbound dialing guard. Enforced before every
            SIP INVITE.
        max_concurrent_calls (int | Unset):  Default: 10.
        media_encryption (SipTrunkCreateMediaEncryption | Unset):  Default: SipTrunkCreateMediaEncryption.ALLOW.
        numbers (list[str] | Unset):
        outbound_address (None | str | Unset):
        transport (SipTrunkCreateTransport | Unset):  Default: SipTrunkCreateTransport.UDP.
    """

    name: str
    type_: SipTrunkCreateType
    allowed_addresses: list[str] | Unset = UNSET
    auth_mode: SipTrunkCreateAuthMode | Unset = SipTrunkCreateAuthMode.DIGEST
    auth_password: None | str | Unset = UNSET
    auth_username: None | str | Unset = UNSET
    calls_per_hour_limit: int | Unset = 1000
    destination_allowlist: DestinationAllowlist | Unset = UNSET
    max_concurrent_calls: int | Unset = 10
    media_encryption: SipTrunkCreateMediaEncryption | Unset = SipTrunkCreateMediaEncryption.ALLOW
    numbers: list[str] | Unset = UNSET
    outbound_address: None | str | Unset = UNSET
    transport: SipTrunkCreateTransport | Unset = SipTrunkCreateTransport.UDP

    def to_dict(self) -> dict[str, Any]:
        from ..models.destination_allowlist import DestinationAllowlist

        name = self.name

        type_ = self.type_.value

        allowed_addresses: list[str] | Unset = UNSET
        if not isinstance(self.allowed_addresses, Unset):
            allowed_addresses = self.allowed_addresses

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

        max_concurrent_calls = self.max_concurrent_calls

        media_encryption: str | Unset = UNSET
        if not isinstance(self.media_encryption, Unset):
            media_encryption = self.media_encryption.value

        numbers: list[str] | Unset = UNSET
        if not isinstance(self.numbers, Unset):
            numbers = self.numbers

        outbound_address: None | str | Unset
        if isinstance(self.outbound_address, Unset):
            outbound_address = UNSET
        else:
            outbound_address = self.outbound_address

        transport: str | Unset = UNSET
        if not isinstance(self.transport, Unset):
            transport = self.transport.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "type": type_,
            }
        )
        if allowed_addresses is not UNSET:
            field_dict["allowed_addresses"] = allowed_addresses
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
        if max_concurrent_calls is not UNSET:
            field_dict["max_concurrent_calls"] = max_concurrent_calls
        if media_encryption is not UNSET:
            field_dict["media_encryption"] = media_encryption
        if numbers is not UNSET:
            field_dict["numbers"] = numbers
        if outbound_address is not UNSET:
            field_dict["outbound_address"] = outbound_address
        if transport is not UNSET:
            field_dict["transport"] = transport

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.destination_allowlist import DestinationAllowlist

        d = dict(src_dict)
        name = d.pop("name")

        type_ = SipTrunkCreateType(d.pop("type"))

        allowed_addresses = cast(list[str], d.pop("allowed_addresses", UNSET))

        _auth_mode = d.pop("auth_mode", UNSET)
        auth_mode: SipTrunkCreateAuthMode | Unset
        if isinstance(_auth_mode, Unset):
            auth_mode = UNSET
        else:
            auth_mode = SipTrunkCreateAuthMode(_auth_mode)

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

        max_concurrent_calls = d.pop("max_concurrent_calls", UNSET)

        _media_encryption = d.pop("media_encryption", UNSET)
        media_encryption: SipTrunkCreateMediaEncryption | Unset
        if isinstance(_media_encryption, Unset):
            media_encryption = UNSET
        else:
            media_encryption = SipTrunkCreateMediaEncryption(_media_encryption)

        numbers = cast(list[str], d.pop("numbers", UNSET))

        def _parse_outbound_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        outbound_address = _parse_outbound_address(d.pop("outbound_address", UNSET))

        _transport = d.pop("transport", UNSET)
        transport: SipTrunkCreateTransport | Unset
        if isinstance(_transport, Unset):
            transport = UNSET
        else:
            transport = SipTrunkCreateTransport(_transport)

        sip_trunk_create = cls(
            name=name,
            type_=type_,
            allowed_addresses=allowed_addresses,
            auth_mode=auth_mode,
            auth_password=auth_password,
            auth_username=auth_username,
            calls_per_hour_limit=calls_per_hour_limit,
            destination_allowlist=destination_allowlist,
            max_concurrent_calls=max_concurrent_calls,
            media_encryption=media_encryption,
            numbers=numbers,
            outbound_address=outbound_address,
            transport=transport,
        )

        return sip_trunk_create
