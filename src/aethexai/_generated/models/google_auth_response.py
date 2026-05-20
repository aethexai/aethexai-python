from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.auth_tokens import AuthTokens
    from ..models.developer_response import DeveloperResponse


T = TypeVar("T", bound="GoogleAuthResponse")


@_attrs_define
class GoogleAuthResponse:
    """
    Attributes:
        developer (DeveloperResponse):
        tokens (AuthTokens):
        api_key (None | str | Unset):
        is_new (bool | Unset):  Default: False.
    """

    developer: DeveloperResponse
    tokens: AuthTokens
    api_key: None | str | Unset = UNSET
    is_new: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_tokens import AuthTokens
        from ..models.developer_response import DeveloperResponse

        developer = self.developer.to_dict()

        tokens = self.tokens.to_dict()

        api_key: None | str | Unset
        if isinstance(self.api_key, Unset):
            api_key = UNSET
        else:
            api_key = self.api_key

        is_new = self.is_new

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "developer": developer,
                "tokens": tokens,
            }
        )
        if api_key is not UNSET:
            field_dict["api_key"] = api_key
        if is_new is not UNSET:
            field_dict["is_new"] = is_new

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_tokens import AuthTokens
        from ..models.developer_response import DeveloperResponse

        d = dict(src_dict)
        developer = DeveloperResponse.from_dict(d.pop("developer"))

        tokens = AuthTokens.from_dict(d.pop("tokens"))

        def _parse_api_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        api_key = _parse_api_key(d.pop("api_key", UNSET))

        is_new = d.pop("is_new", UNSET)

        google_auth_response = cls(
            developer=developer,
            tokens=tokens,
            api_key=api_key,
            is_new=is_new,
        )

        google_auth_response.additional_properties = d
        return google_auth_response

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
