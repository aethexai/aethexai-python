from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="TwilioAccountCreate")


@_attrs_define
class TwilioAccountCreate:
    """Request body for ``POST /api/v1/twilio-accounts``.

    ``auth_token`` is required at registration time so we can verify the
    SID/token pair with Twilio before persisting.

        Attributes:
            account_sid (str):
            auth_token (str):
            friendly_name (str | Unset):  Default: ''.
    """

    account_sid: str
    auth_token: str
    friendly_name: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_sid = self.account_sid

        auth_token = self.auth_token

        friendly_name = self.friendly_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_sid": account_sid,
                "auth_token": auth_token,
            }
        )
        if friendly_name is not UNSET:
            field_dict["friendly_name"] = friendly_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        account_sid = d.pop("account_sid")

        auth_token = d.pop("auth_token")

        friendly_name = d.pop("friendly_name", UNSET)

        twilio_account_create = cls(
            account_sid=account_sid,
            auth_token=auth_token,
            friendly_name=friendly_name,
        )

        twilio_account_create.additional_properties = d
        return twilio_account_create

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
