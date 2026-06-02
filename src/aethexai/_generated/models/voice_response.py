from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="VoiceResponse")


@_attrs_define
class VoiceResponse:
    """
    Attributes:
        id (str):
        name (str):
        country (None | str | Unset):
        description (None | str | Unset):
        gender (str | Unset):  Default: ''.
        is_cloned (bool | Unset):  Default: False.
        language (str | Unset):  Default: ''.
        preview_url (None | str | Unset):
        supports_dialect_style (bool | Unset):  Default: False.
        tags (list[str] | Unset):
    """

    id: str
    name: str
    country: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    gender: str | Unset = ""
    is_cloned: bool | Unset = False
    language: str | Unset = ""
    preview_url: None | str | Unset = UNSET
    supports_dialect_style: bool | Unset = False
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        country: None | str | Unset
        if isinstance(self.country, Unset):
            country = UNSET
        else:
            country = self.country

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        gender = self.gender

        is_cloned = self.is_cloned

        language = self.language

        preview_url: None | str | Unset
        if isinstance(self.preview_url, Unset):
            preview_url = UNSET
        else:
            preview_url = self.preview_url

        supports_dialect_style = self.supports_dialect_style

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if country is not UNSET:
            field_dict["country"] = country
        if description is not UNSET:
            field_dict["description"] = description
        if gender is not UNSET:
            field_dict["gender"] = gender
        if is_cloned is not UNSET:
            field_dict["is_cloned"] = is_cloned
        if language is not UNSET:
            field_dict["language"] = language
        if preview_url is not UNSET:
            field_dict["preview_url"] = preview_url
        if supports_dialect_style is not UNSET:
            field_dict["supports_dialect_style"] = supports_dialect_style
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_country(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        country = _parse_country(d.pop("country", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        gender = d.pop("gender", UNSET)

        is_cloned = d.pop("is_cloned", UNSET)

        language = d.pop("language", UNSET)

        def _parse_preview_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        preview_url = _parse_preview_url(d.pop("preview_url", UNSET))

        supports_dialect_style = d.pop("supports_dialect_style", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        voice_response = cls(
            id=id,
            name=name,
            country=country,
            description=description,
            gender=gender,
            is_cloned=is_cloned,
            language=language,
            preview_url=preview_url,
            supports_dialect_style=supports_dialect_style,
            tags=tags,
        )

        voice_response.additional_properties = d
        return voice_response

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
