from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="SmallWebRTCRequest")


@_attrs_define
class SmallWebRTCRequest:
    """
    Attributes:
        sdp (str):
        type_ (str):
        pc_id (None | str | Unset):
        request_data (Any | None | Unset):
        restart_pc (bool | None | Unset):
    """

    sdp: str
    type_: str
    pc_id: None | str | Unset = UNSET
    request_data: Any | None | Unset = UNSET
    restart_pc: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sdp = self.sdp

        type_ = self.type_

        pc_id: None | str | Unset
        if isinstance(self.pc_id, Unset):
            pc_id = UNSET
        else:
            pc_id = self.pc_id

        request_data: Any | None | Unset
        if isinstance(self.request_data, Unset):
            request_data = UNSET
        else:
            request_data = self.request_data

        restart_pc: bool | None | Unset
        if isinstance(self.restart_pc, Unset):
            restart_pc = UNSET
        else:
            restart_pc = self.restart_pc

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sdp": sdp,
                "type": type_,
            }
        )
        if pc_id is not UNSET:
            field_dict["pc_id"] = pc_id
        if request_data is not UNSET:
            field_dict["request_data"] = request_data
        if restart_pc is not UNSET:
            field_dict["restart_pc"] = restart_pc

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sdp = d.pop("sdp")

        type_ = d.pop("type")

        def _parse_pc_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pc_id = _parse_pc_id(d.pop("pc_id", UNSET))

        def _parse_request_data(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        request_data = _parse_request_data(d.pop("request_data", UNSET))

        def _parse_restart_pc(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        restart_pc = _parse_restart_pc(d.pop("restart_pc", UNSET))

        small_web_rtc_request = cls(
            sdp=sdp,
            type_=type_,
            pc_id=pc_id,
            request_data=request_data,
            restart_pc=restart_pc,
        )

        small_web_rtc_request.additional_properties = d
        return small_web_rtc_request

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
