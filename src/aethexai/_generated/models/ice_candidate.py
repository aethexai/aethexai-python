from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


T = TypeVar("T", bound="IceCandidate")


@_attrs_define
class IceCandidate:
    """The remote ice candidate object received from the peer connection.

    Parameters:
        candidate: The ice candidate patch SDP string (Session Description Protocol).
        sdp_mid: The SDP mid for the candidate patch.
        sdp_mline_index: The SDP mline index for the candidate patch.

        Attributes:
            candidate (str):
            sdp_mid (str):
            sdp_mline_index (int):
    """

    candidate: str
    sdp_mid: str
    sdp_mline_index: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        candidate = self.candidate

        sdp_mid = self.sdp_mid

        sdp_mline_index = self.sdp_mline_index

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "candidate": candidate,
                "sdp_mid": sdp_mid,
                "sdp_mline_index": sdp_mline_index,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        candidate = d.pop("candidate")

        sdp_mid = d.pop("sdp_mid")

        sdp_mline_index = d.pop("sdp_mline_index")

        ice_candidate = cls(
            candidate=candidate,
            sdp_mid=sdp_mid,
            sdp_mline_index=sdp_mline_index,
        )

        ice_candidate.additional_properties = d
        return ice_candidate

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
