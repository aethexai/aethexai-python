from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="TwilioAccountResponse")


@_attrs_define
class TwilioAccountResponse:
    """Response shape. ``auth_token`` is never returned. ``tenant_id`` is ``None`` for platform-shared credentials (any
    tenant
    can attach numbers) and a UUID string for tenant-owned (BYO) rows.

        Attributes:
            account_sid (str):
            id (str):
            status (str):
            created_at (None | str | Unset):
            friendly_name (str | Unset):  Default: ''.
            tenant_id (None | str | Unset):
            updated_at (None | str | Unset):
    """

    account_sid: str
    id: str
    status: str
    created_at: None | str | Unset = UNSET
    friendly_name: str | Unset = ""
    tenant_id: None | str | Unset = UNSET
    updated_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_sid = self.account_sid

        id = self.id

        status = self.status

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        friendly_name = self.friendly_name

        tenant_id: None | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        else:
            tenant_id = self.tenant_id

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_sid": account_sid,
                "id": id,
                "status": status,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if friendly_name is not UNSET:
            field_dict["friendly_name"] = friendly_name
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        account_sid = d.pop("account_sid")

        id = d.pop("id")

        status = d.pop("status")

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        friendly_name = d.pop("friendly_name", UNSET)

        def _parse_tenant_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tenant_id = _parse_tenant_id(d.pop("tenant_id", UNSET))

        def _parse_updated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        twilio_account_response = cls(
            account_sid=account_sid,
            id=id,
            status=status,
            created_at=created_at,
            friendly_name=friendly_name,
            tenant_id=tenant_id,
            updated_at=updated_at,
        )

        twilio_account_response.additional_properties = d
        return twilio_account_response

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
