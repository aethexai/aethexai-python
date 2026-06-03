from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="APIKeyResponse")


@_attrs_define
class APIKeyResponse:
    """
    Attributes:
        id (str):
        key_prefix (str):
        name (str):
        rate_limit_daily (int):
        rate_limit_rpm (int):
        scopes (list[str]):
        created_at (None | str | Unset):
        expires_at (None | str | Unset):
        is_active (bool | Unset):  Default: True.
        key (None | str | Unset):
        last_used_at (None | str | Unset):
        revoked_at (None | str | Unset):
        usage_count (int | Unset):  Default: 0.
    """

    id: str
    key_prefix: str
    name: str
    rate_limit_daily: int
    rate_limit_rpm: int
    scopes: list[str]
    created_at: None | str | Unset = UNSET
    expires_at: None | str | Unset = UNSET
    is_active: bool | Unset = True
    key: None | str | Unset = UNSET
    last_used_at: None | str | Unset = UNSET
    revoked_at: None | str | Unset = UNSET
    usage_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        key_prefix = self.key_prefix

        name = self.name

        rate_limit_daily = self.rate_limit_daily

        rate_limit_rpm = self.rate_limit_rpm

        scopes = self.scopes

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = self.expires_at

        is_active = self.is_active

        key: None | str | Unset
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        else:
            last_used_at = self.last_used_at

        revoked_at: None | str | Unset
        if isinstance(self.revoked_at, Unset):
            revoked_at = UNSET
        else:
            revoked_at = self.revoked_at

        usage_count = self.usage_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "key_prefix": key_prefix,
                "name": name,
                "rate_limit_daily": rate_limit_daily,
                "rate_limit_rpm": rate_limit_rpm,
                "scopes": scopes,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if key is not UNSET:
            field_dict["key"] = key
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if revoked_at is not UNSET:
            field_dict["revoked_at"] = revoked_at
        if usage_count is not UNSET:
            field_dict["usage_count"] = usage_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        key_prefix = d.pop("key_prefix")

        name = d.pop("name")

        rate_limit_daily = d.pop("rate_limit_daily")

        rate_limit_rpm = d.pop("rate_limit_rpm")

        scopes = cast(list[str], d.pop("scopes"))

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_expires_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        is_active = d.pop("is_active", UNSET)

        def _parse_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        key = _parse_key(d.pop("key", UNSET))

        def _parse_last_used_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at", UNSET))

        def _parse_revoked_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        revoked_at = _parse_revoked_at(d.pop("revoked_at", UNSET))

        usage_count = d.pop("usage_count", UNSET)

        api_key_response = cls(
            id=id,
            key_prefix=key_prefix,
            name=name,
            rate_limit_daily=rate_limit_daily,
            rate_limit_rpm=rate_limit_rpm,
            scopes=scopes,
            created_at=created_at,
            expires_at=expires_at,
            is_active=is_active,
            key=key,
            last_used_at=last_used_at,
            revoked_at=revoked_at,
            usage_count=usage_count,
        )

        api_key_response.additional_properties = d
        return api_key_response

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
