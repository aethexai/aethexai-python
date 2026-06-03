from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="TTSRequest")


@_attrs_define
class TTSRequest:
    """
    Attributes:
        text (str):
        language (str | Unset):  Default: 'english'.
        streaming (bool | Unset):  Default: False.
        voice_id (None | str | Unset):
    """

    text: str
    language: str | Unset = "english"
    streaming: bool | Unset = False
    voice_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        language = self.language

        streaming = self.streaming

        voice_id: None | str | Unset
        if isinstance(self.voice_id, Unset):
            voice_id = UNSET
        else:
            voice_id = self.voice_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
            }
        )
        if language is not UNSET:
            field_dict["language"] = language
        if streaming is not UNSET:
            field_dict["streaming"] = streaming
        if voice_id is not UNSET:
            field_dict["voice_id"] = voice_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        text = d.pop("text")

        language = d.pop("language", UNSET)

        streaming = d.pop("streaming", UNSET)

        def _parse_voice_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        voice_id = _parse_voice_id(d.pop("voice_id", UNSET))

        tts_request = cls(
            text=text,
            language=language,
            streaming=streaming,
            voice_id=voice_id,
        )

        tts_request.additional_properties = d
        return tts_request

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
