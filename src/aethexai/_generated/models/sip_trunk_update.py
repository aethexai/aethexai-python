from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sip_trunk_update_auth_mode_type_0 import SipTrunkUpdateAuthModeType0
from ..models.sip_trunk_update_status_type_0 import SipTrunkUpdateStatusType0
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.destination_allowlist import DestinationAllowlist


T = TypeVar("T", bound="SipTrunkUpdate")


@_attrs_define
class SipTrunkUpdate:
    """
    Attributes:
        allowed_addresses (list[str] | None | Unset):
        auth_mode (None | SipTrunkUpdateAuthModeType0 | Unset):
        calls_per_hour_limit (int | None | Unset):
        destination_allowlist (DestinationAllowlist | None | Unset):
        max_concurrent_calls (int | None | Unset):
        name (None | str | Unset):
        numbers (list[str] | None | Unset):
        status (None | SipTrunkUpdateStatusType0 | Unset):
    """

    allowed_addresses: list[str] | None | Unset = UNSET
    auth_mode: None | SipTrunkUpdateAuthModeType0 | Unset = UNSET
    calls_per_hour_limit: int | None | Unset = UNSET
    destination_allowlist: DestinationAllowlist | None | Unset = UNSET
    max_concurrent_calls: int | None | Unset = UNSET
    name: None | str | Unset = UNSET
    numbers: list[str] | None | Unset = UNSET
    status: None | SipTrunkUpdateStatusType0 | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.destination_allowlist import DestinationAllowlist

        allowed_addresses: list[str] | None | Unset
        if isinstance(self.allowed_addresses, Unset):
            allowed_addresses = UNSET
        elif isinstance(self.allowed_addresses, list):
            allowed_addresses = self.allowed_addresses

        else:
            allowed_addresses = self.allowed_addresses

        auth_mode: None | str | Unset
        if isinstance(self.auth_mode, Unset):
            auth_mode = UNSET
        elif isinstance(self.auth_mode, SipTrunkUpdateAuthModeType0):
            auth_mode = self.auth_mode.value
        else:
            auth_mode = self.auth_mode

        calls_per_hour_limit: int | None | Unset
        if isinstance(self.calls_per_hour_limit, Unset):
            calls_per_hour_limit = UNSET
        else:
            calls_per_hour_limit = self.calls_per_hour_limit

        destination_allowlist: dict[str, Any] | None | Unset
        if isinstance(self.destination_allowlist, Unset):
            destination_allowlist = UNSET
        elif isinstance(self.destination_allowlist, DestinationAllowlist):
            destination_allowlist = self.destination_allowlist.to_dict()
        else:
            destination_allowlist = self.destination_allowlist

        max_concurrent_calls: int | None | Unset
        if isinstance(self.max_concurrent_calls, Unset):
            max_concurrent_calls = UNSET
        else:
            max_concurrent_calls = self.max_concurrent_calls

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        numbers: list[str] | None | Unset
        if isinstance(self.numbers, Unset):
            numbers = UNSET
        elif isinstance(self.numbers, list):
            numbers = self.numbers

        else:
            numbers = self.numbers

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, SipTrunkUpdateStatusType0):
            status = self.status.value
        else:
            status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if allowed_addresses is not UNSET:
            field_dict["allowed_addresses"] = allowed_addresses
        if auth_mode is not UNSET:
            field_dict["auth_mode"] = auth_mode
        if calls_per_hour_limit is not UNSET:
            field_dict["calls_per_hour_limit"] = calls_per_hour_limit
        if destination_allowlist is not UNSET:
            field_dict["destination_allowlist"] = destination_allowlist
        if max_concurrent_calls is not UNSET:
            field_dict["max_concurrent_calls"] = max_concurrent_calls
        if name is not UNSET:
            field_dict["name"] = name
        if numbers is not UNSET:
            field_dict["numbers"] = numbers
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.destination_allowlist import DestinationAllowlist

        d = dict(src_dict)

        def _parse_allowed_addresses(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_addresses_type_0 = cast(list[str], data)

                return allowed_addresses_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        allowed_addresses = _parse_allowed_addresses(d.pop("allowed_addresses", UNSET))

        def _parse_auth_mode(data: object) -> None | SipTrunkUpdateAuthModeType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                auth_mode_type_0 = SipTrunkUpdateAuthModeType0(data)

                return auth_mode_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SipTrunkUpdateAuthModeType0 | Unset, data)

        auth_mode = _parse_auth_mode(d.pop("auth_mode", UNSET))

        def _parse_calls_per_hour_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        calls_per_hour_limit = _parse_calls_per_hour_limit(d.pop("calls_per_hour_limit", UNSET))

        def _parse_destination_allowlist(data: object) -> DestinationAllowlist | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                destination_allowlist_type_0 = DestinationAllowlist.from_dict(data)

                return destination_allowlist_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DestinationAllowlist | None | Unset, data)

        destination_allowlist = _parse_destination_allowlist(d.pop("destination_allowlist", UNSET))

        def _parse_max_concurrent_calls(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_concurrent_calls = _parse_max_concurrent_calls(d.pop("max_concurrent_calls", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_numbers(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                numbers_type_0 = cast(list[str], data)

                return numbers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        numbers = _parse_numbers(d.pop("numbers", UNSET))

        def _parse_status(data: object) -> None | SipTrunkUpdateStatusType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = SipTrunkUpdateStatusType0(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SipTrunkUpdateStatusType0 | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        sip_trunk_update = cls(
            allowed_addresses=allowed_addresses,
            auth_mode=auth_mode,
            calls_per_hour_limit=calls_per_hour_limit,
            destination_allowlist=destination_allowlist,
            max_concurrent_calls=max_concurrent_calls,
            name=name,
            numbers=numbers,
            status=status,
        )

        return sip_trunk_update
