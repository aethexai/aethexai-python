from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO
from typing import cast


T = TypeVar("T", bound="BodyUploadKnowledgeDocApiV1AgentsAgentIdKnowledgeBasePost")


@_attrs_define
class BodyUploadKnowledgeDocApiV1AgentsAgentIdKnowledgeBasePost:
    """
    Attributes:
        file (File | None | Unset):
        filename (None | str | Unset):
        text (None | str | Unset):
    """

    file: File | None | Unset = UNSET
    filename: None | str | Unset = UNSET
    text: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file: FileTypes | None | Unset
        if isinstance(self.file, Unset):
            file = UNSET
        elif isinstance(self.file, File):
            file = self.file.to_tuple()

        else:
            file = self.file

        filename: None | str | Unset
        if isinstance(self.filename, Unset):
            filename = UNSET
        else:
            filename = self.filename

        text: None | str | Unset
        if isinstance(self.text, Unset):
            text = UNSET
        else:
            text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if file is not UNSET:
            field_dict["file"] = file
        if filename is not UNSET:
            field_dict["filename"] = filename
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.file, Unset):
            if isinstance(self.file, File):
                files.append(("file", self.file.to_tuple()))
            else:
                files.append(("file", (None, str(self.file).encode(), "text/plain")))

        if not isinstance(self.filename, Unset):
            if isinstance(self.filename, str):
                files.append(("filename", (None, str(self.filename).encode(), "text/plain")))
            else:
                files.append(("filename", (None, str(self.filename).encode(), "text/plain")))

        if not isinstance(self.text, Unset):
            if isinstance(self.text, str):
                files.append(("text", (None, str(self.text).encode(), "text/plain")))
            else:
                files.append(("text", (None, str(self.text).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_file(data: object) -> File | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                file_type_0 = File(payload=BytesIO(data))

                return file_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(File | None | Unset, data)

        file = _parse_file(d.pop("file", UNSET))

        def _parse_filename(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filename = _parse_filename(d.pop("filename", UNSET))

        def _parse_text(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        text = _parse_text(d.pop("text", UNSET))

        body_upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post = cls(
            file=file,
            filename=filename,
            text=text,
        )

        body_upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post.additional_properties = d
        return body_upload_knowledge_doc_api_v1_agents_agent_id_knowledge_base_post

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
