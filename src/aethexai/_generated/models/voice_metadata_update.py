from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.voice_gender import VoiceGender
from ..models.voice_metadata_update_status_type_0 import VoiceMetadataUpdateStatusType0
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="VoiceMetadataUpdate")


@_attrs_define
class VoiceMetadataUpdate:
    """Body for ``PATCH /internal/voices/{voice_key}``.

    Editable fields:

    * ``display_name``: curator-authored override for the customer-facing
      voice name. The migrated ``name`` value is the durable fallback;
      setting this to ``null`` clears the override and the response reverts
      to the migrated name.
    * ``status``: soft-retire flag. ``"active"`` shows the voice on
      ``GET /voices``; ``"retired"`` hides it from listings and 404s
      ``GET /voices/{voice_id}`` while leaving the row (and the internal
      voice-registry consumed by the TTS pod) untouched.
    * ``description``: customer-facing one-liner. Brand-leak validated
      like ``display_name``.
    * ``internal_notes``: admin-only commentary, never copied onto the
      public ``VoiceResponse``. No brand-leak scrub because the field is
      meant to hold context that legitimately names internal voices.
    * ``tags``: closed-vocabulary list of tokens drawn from
      :data:`VOICE_TAG_VOCABULARY`. Send ``[]`` to clear; sending
      ``null`` is rejected because the underlying column is NOT NULL.
    * ``gender``: curator-authored correction for the speaker's perceived
      gender. The seed gender is best-effort and is known to be wrong on
      some pool voices, so the dashboard exposes a male/female/neutral
      selector that PATCHes the canonical value here. Sending ``null``
      is rejected because the underlying column is NOT NULL; omit the
      key to leave the existing value unchanged.

    Every field is optional. Omitting a key leaves the column untouched
    via ``model_dump(exclude_unset=True)``; sending ``null`` on a
    nullable field clears it.

    Unknown keys are intentionally tolerated (``extra='ignore'``, the
    Pydantic default) so a rolling deploy stays safe: during the window
    between an API rollout that adds a new metadata field and the
    matching dashboard rollout, a dashboard PATCH that still sends an
    older shape (or, in the reverse direction, a dashboard that already
    sends a newer field name) must not 422 the curator out of a save.
    The trade-off is that a typo in a hand-rolled curator script
    silently no-ops the misspelled key; the dashboard form is the only
    real client and is exercised end-to-end before each deploy.

        Attributes:
            description (None | str | Unset):
            display_name (None | str | Unset):
            gender (None | Unset | VoiceGender):
            internal_notes (None | str | Unset):
            status (None | Unset | VoiceMetadataUpdateStatusType0):
            tags (list[str] | None | Unset):
    """

    description: None | str | Unset = UNSET
    display_name: None | str | Unset = UNSET
    gender: None | Unset | VoiceGender = UNSET
    internal_notes: None | str | Unset = UNSET
    status: None | Unset | VoiceMetadataUpdateStatusType0 = UNSET
    tags: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        gender: None | str | Unset
        if isinstance(self.gender, Unset):
            gender = UNSET
        elif isinstance(self.gender, VoiceGender):
            gender = self.gender.value
        else:
            gender = self.gender

        internal_notes: None | str | Unset
        if isinstance(self.internal_notes, Unset):
            internal_notes = UNSET
        else:
            internal_notes = self.internal_notes

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, VoiceMetadataUpdateStatusType0):
            status = self.status.value
        else:
            status = self.status

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if gender is not UNSET:
            field_dict["gender"] = gender
        if internal_notes is not UNSET:
            field_dict["internal_notes"] = internal_notes
        if status is not UNSET:
            field_dict["status"] = status
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

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

        def _parse_gender(data: object) -> None | Unset | VoiceGender:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                gender_type_0 = VoiceGender(data)

                return gender_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | VoiceGender, data)

        gender = _parse_gender(d.pop("gender", UNSET))

        def _parse_internal_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        internal_notes = _parse_internal_notes(d.pop("internal_notes", UNSET))

        def _parse_status(data: object) -> None | Unset | VoiceMetadataUpdateStatusType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = VoiceMetadataUpdateStatusType0(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | VoiceMetadataUpdateStatusType0, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        voice_metadata_update = cls(
            description=description,
            display_name=display_name,
            gender=gender,
            internal_notes=internal_notes,
            status=status,
            tags=tags,
        )

        voice_metadata_update.additional_properties = d
        return voice_metadata_update

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
