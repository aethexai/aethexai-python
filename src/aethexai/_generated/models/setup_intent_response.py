from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


T = TypeVar("T", bound="SetupIntentResponse")


@_attrs_define
class SetupIntentResponse:
    """Returned to the portal so the Payment Element can confirm card
    details. The ``client_secret`` is the one secret the portal needs
    to drive the Stripe Element; never log it server-side.

        Attributes:
            client_secret (str): Stripe SetupIntent client_secret. Pass to the portal Payment Element as the
                ``clientSecret`` option.
            publishable_key (str): Stripe publishable key (``pk_*``). Surfaced in the same response so the portal doesn't
                need a separate /config call.
            setup_intent_id (str):
    """

    client_secret: str
    publishable_key: str
    setup_intent_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_secret = self.client_secret

        publishable_key = self.publishable_key

        setup_intent_id = self.setup_intent_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_secret": client_secret,
                "publishable_key": publishable_key,
                "setup_intent_id": setup_intent_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_secret = d.pop("client_secret")

        publishable_key = d.pop("publishable_key")

        setup_intent_id = d.pop("setup_intent_id")

        setup_intent_response = cls(
            client_secret=client_secret,
            publishable_key=publishable_key,
            setup_intent_id=setup_intent_id,
        )

        setup_intent_response.additional_properties = d
        return setup_intent_response

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
