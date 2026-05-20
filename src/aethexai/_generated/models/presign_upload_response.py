from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.presign_upload_response_headers import PresignUploadResponseHeaders


T = TypeVar("T", bound="PresignUploadResponse")


@_attrs_define
class PresignUploadResponse:
    """
    Attributes:
        expires_at (str):
        headers (PresignUploadResponseHeaders):
        max_bytes (int):
        method (str):
        upload_id (str):
        upload_url (str):
    """

    expires_at: str
    headers: PresignUploadResponseHeaders
    max_bytes: int
    method: str
    upload_id: str
    upload_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.presign_upload_response_headers import PresignUploadResponseHeaders

        expires_at = self.expires_at

        headers = self.headers.to_dict()

        max_bytes = self.max_bytes

        method = self.method

        upload_id = self.upload_id

        upload_url = self.upload_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expires_at": expires_at,
                "headers": headers,
                "max_bytes": max_bytes,
                "method": method,
                "upload_id": upload_id,
                "upload_url": upload_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.presign_upload_response_headers import PresignUploadResponseHeaders

        d = dict(src_dict)
        expires_at = d.pop("expires_at")

        headers = PresignUploadResponseHeaders.from_dict(d.pop("headers"))

        max_bytes = d.pop("max_bytes")

        method = d.pop("method")

        upload_id = d.pop("upload_id")

        upload_url = d.pop("upload_url")

        presign_upload_response = cls(
            expires_at=expires_at,
            headers=headers,
            max_bytes=max_bytes,
            method=method,
            upload_id=upload_id,
            upload_url=upload_url,
        )

        presign_upload_response.additional_properties = d
        return presign_upload_response

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
