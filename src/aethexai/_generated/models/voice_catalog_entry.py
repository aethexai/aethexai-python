from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.voice_catalog_entry_status import VoiceCatalogEntryStatus
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="VoiceCatalogEntry")


@_attrs_define
class VoiceCatalogEntry:
    """Admin-only response shape returned by the internal PATCH endpoint
    and the admin listing at ``GET /internal/voices``.

    Mirrors ``VoiceResponse`` and adds the curator-only fields:

    * ``voice_type`` (curator-only, dropped from the public surface in
      PR #978: customers cannot switch on materialisation type, but the
      curator dashboard, CI smoke discovery, and the integration-test
      fixture all need it to distinguish ``icl`` / ``singlespeaker`` /
      ``multispeaker``)
    * ``display_name`` (curator override; folded into ``name`` on the
      public response via ``Voice.public_name``)
    * ``internal_notes`` (admin-only; never copied onto the public
      response)
    * ``status`` (soft-retire flag; surfaced here so curators can
      flip it round-trip without a follow-up GET)

    ``model_size`` is absent from BOTH shapes: it was dropped from the
    public response in PR #978 and the PATCH handler does not join
    ``TtsModel`` so the value is not available here either.

    WARNING: ``internal_notes`` must never appear on a public
    ``response_model``. It is intentionally excluded from
    ``_voice_to_response``; verify any new route that uses this class
    sits behind the ``/internal`` auth boundary (either
    ``require_internal_auth`` or ``require_admin``).

        Attributes:
            id (str):
            name (str):
            status (VoiceCatalogEntryStatus):
            country (None | str | Unset):
            description (None | str | Unset):
            display_name (None | str | Unset):
            gender (str | Unset):  Default: ''.
            internal_notes (None | str | Unset):
            is_cloned (bool | Unset):  Default: False.
            language (str | Unset):  Default: ''.
            preview_url (None | str | Unset):
            supports_dialect_style (bool | Unset):  Default: False.
            tags (list[str] | Unset):
            voice_type (str | Unset):  Default: 'icl'.
    """

    id: str
    name: str
    status: VoiceCatalogEntryStatus
    country: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    display_name: None | str | Unset = UNSET
    gender: str | Unset = ""
    internal_notes: None | str | Unset = UNSET
    is_cloned: bool | Unset = False
    language: str | Unset = ""
    preview_url: None | str | Unset = UNSET
    supports_dialect_style: bool | Unset = False
    tags: list[str] | Unset = UNSET
    voice_type: str | Unset = "icl"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        status = self.status.value

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

        display_name: None | str | Unset
        if isinstance(self.display_name, Unset):
            display_name = UNSET
        else:
            display_name = self.display_name

        gender = self.gender

        internal_notes: None | str | Unset
        if isinstance(self.internal_notes, Unset):
            internal_notes = UNSET
        else:
            internal_notes = self.internal_notes

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

        voice_type = self.voice_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "status": status,
            }
        )
        if country is not UNSET:
            field_dict["country"] = country
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if gender is not UNSET:
            field_dict["gender"] = gender
        if internal_notes is not UNSET:
            field_dict["internal_notes"] = internal_notes
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
        if voice_type is not UNSET:
            field_dict["voice_type"] = voice_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        status = VoiceCatalogEntryStatus(d.pop("status"))

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

        def _parse_display_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        display_name = _parse_display_name(d.pop("display_name", UNSET))

        gender = d.pop("gender", UNSET)

        def _parse_internal_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        internal_notes = _parse_internal_notes(d.pop("internal_notes", UNSET))

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

        voice_type = d.pop("voice_type", UNSET)

        voice_catalog_entry = cls(
            id=id,
            name=name,
            status=status,
            country=country,
            description=description,
            display_name=display_name,
            gender=gender,
            internal_notes=internal_notes,
            is_cloned=is_cloned,
            language=language,
            preview_url=preview_url,
            supports_dialect_style=supports_dialect_style,
            tags=tags,
            voice_type=voice_type,
        )

        voice_catalog_entry.additional_properties = d
        return voice_catalog_entry

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
