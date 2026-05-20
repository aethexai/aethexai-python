from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="TwilioRegisterRequest")


@_attrs_define
class TwilioRegisterRequest:
    """
    Attributes:
        phone_number (str):
        twilio_account_id (str):
        agent_id (None | str | Unset):
        friendly_name (str | Unset):  Default: ''.
    """

    phone_number: str
    twilio_account_id: str
    agent_id: None | str | Unset = UNSET
    friendly_name: str | Unset = ""

    def to_dict(self) -> dict[str, Any]:
        phone_number = self.phone_number

        twilio_account_id = self.twilio_account_id

        agent_id: None | str | Unset
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        else:
            agent_id = self.agent_id

        friendly_name = self.friendly_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "phone_number": phone_number,
                "twilio_account_id": twilio_account_id,
            }
        )
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if friendly_name is not UNSET:
            field_dict["friendly_name"] = friendly_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phone_number = d.pop("phone_number")

        twilio_account_id = d.pop("twilio_account_id")

        def _parse_agent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_id = _parse_agent_id(d.pop("agent_id", UNSET))

        friendly_name = d.pop("friendly_name", UNSET)

        twilio_register_request = cls(
            phone_number=phone_number,
            twilio_account_id=twilio_account_id,
            agent_id=agent_id,
            friendly_name=friendly_name,
        )

        return twilio_register_request
