from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.presign_upload_request_kind import PresignUploadRequestKind
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="PresignUploadRequest")


@_attrs_define
class PresignUploadRequest:
    """Ask the server for a presigned URL the client can PUT a file to.

    Attributes:
        content_type (str):
        kind (PresignUploadRequestKind):
        filename (None | str | Unset):
        size_hint (int | None | Unset):
    """

    content_type: str
    kind: PresignUploadRequestKind
    filename: None | str | Unset = UNSET
    size_hint: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        kind = self.kind.value

        filename: None | str | Unset
        if isinstance(self.filename, Unset):
            filename = UNSET
        else:
            filename = self.filename

        size_hint: int | None | Unset
        if isinstance(self.size_hint, Unset):
            size_hint = UNSET
        else:
            size_hint = self.size_hint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content_type": content_type,
                "kind": kind,
            }
        )
        if filename is not UNSET:
            field_dict["filename"] = filename
        if size_hint is not UNSET:
            field_dict["size_hint"] = size_hint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_type = d.pop("content_type")

        kind = PresignUploadRequestKind(d.pop("kind"))

        def _parse_filename(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filename = _parse_filename(d.pop("filename", UNSET))

        def _parse_size_hint(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        size_hint = _parse_size_hint(d.pop("size_hint", UNSET))

        presign_upload_request = cls(
            content_type=content_type,
            kind=kind,
            filename=filename,
            size_hint=size_hint,
        )

        presign_upload_request.additional_properties = d
        return presign_upload_request

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
