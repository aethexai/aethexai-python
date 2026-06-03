from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="DeveloperResponse")


@_attrs_define
class DeveloperResponse:
    """
    Attributes:
        email (str):
        id (str):
        name (str):
        company (None | str | Unset):
        created_at (None | str | Unset):
        email_verified (bool | Unset):  Default: False.
        google_id (None | str | Unset):
        last_login (None | str | Unset):
        status (str | Unset):  Default: 'active'.
    """

    email: str
    id: str
    name: str
    company: None | str | Unset = UNSET
    created_at: None | str | Unset = UNSET
    email_verified: bool | Unset = False
    google_id: None | str | Unset = UNSET
    last_login: None | str | Unset = UNSET
    status: str | Unset = "active"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        id = self.id

        name = self.name

        company: None | str | Unset
        if isinstance(self.company, Unset):
            company = UNSET
        else:
            company = self.company

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        email_verified = self.email_verified

        google_id: None | str | Unset
        if isinstance(self.google_id, Unset):
            google_id = UNSET
        else:
            google_id = self.google_id

        last_login: None | str | Unset
        if isinstance(self.last_login, Unset):
            last_login = UNSET
        else:
            last_login = self.last_login

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "id": id,
                "name": name,
            }
        )
        if company is not UNSET:
            field_dict["company"] = company
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if email_verified is not UNSET:
            field_dict["email_verified"] = email_verified
        if google_id is not UNSET:
            field_dict["google_id"] = google_id
        if last_login is not UNSET:
            field_dict["last_login"] = last_login
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        id = d.pop("id")

        name = d.pop("name")

        def _parse_company(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        company = _parse_company(d.pop("company", UNSET))

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        email_verified = d.pop("email_verified", UNSET)

        def _parse_google_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        google_id = _parse_google_id(d.pop("google_id", UNSET))

        def _parse_last_login(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_login = _parse_last_login(d.pop("last_login", UNSET))

        status = d.pop("status", UNSET)

        developer_response = cls(
            email=email,
            id=id,
            name=name,
            company=company,
            created_at=created_at,
            email_verified=email_verified,
            google_id=google_id,
            last_login=last_login,
            status=status,
        )

        developer_response.additional_properties = d
        return developer_response

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
