from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.destination_allowlist_mode import DestinationAllowlistMode
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="DestinationAllowlist")


@_attrs_define
class DestinationAllowlist:
    """Per-trunk outbound dialing guard. Enforced before every SIP INVITE.

    Attributes:
        entries (list[str] | Unset): E.164 prefixes. `+1800` matches every US toll-free destination.
        mode (DestinationAllowlistMode | Unset):  Default: DestinationAllowlistMode.BLOCKLIST.
    """

    entries: list[str] | Unset = UNSET
    mode: DestinationAllowlistMode | Unset = DestinationAllowlistMode.BLOCKLIST

    def to_dict(self) -> dict[str, Any]:
        entries: list[str] | Unset = UNSET
        if not isinstance(self.entries, Unset):
            entries = self.entries

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if entries is not UNSET:
            field_dict["entries"] = entries
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        entries = cast(list[str], d.pop("entries", UNSET))

        _mode = d.pop("mode", UNSET)
        mode: DestinationAllowlistMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = DestinationAllowlistMode(_mode)

        destination_allowlist = cls(
            entries=entries,
            mode=mode,
        )

        return destination_allowlist
