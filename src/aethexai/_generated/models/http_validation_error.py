from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.validation_error import ValidationError


T = TypeVar("T", bound="HTTPValidationError")


@_attrs_define
class HTTPValidationError:
    """
    Attributes:
        detail (list[ValidationError] | Unset):
    """

    detail: list[ValidationError] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.validation_error import ValidationError

        detail: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.detail, Unset):
            detail = []
            for detail_item_data in self.detail:
                detail_item = detail_item_data.to_dict()
                detail.append(detail_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if detail is not UNSET:
            field_dict["detail"] = detail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.validation_error import ValidationError

        # aethexai-error-envelope-tolerant: accept the unified error envelope on 422.
        # The OpenAPI spec types 422 as FastAPI's ``HTTPValidationError``
        # (``detail: list[ValidationError]``), but the real API returns
        # ``{error, code, detail: <string>, request_id}``. Without this guard,
        # ``ValidationError.from_dict(<string>)`` crashes with a ``ValueError``
        # from ``dict(src_dict)``. The generated ``_parse_response`` then
        # propagates the crash to ``_call``, which never reaches
        # ``_map_status_to_exception`` and never raises the documented
        # ``aethexai.ValidationError``. By leaving ``detail`` as ``UNSET`` when
        # it isn't list-of-dicts shaped, and stashing the envelope in
        # ``additional_properties``, ``_parse_response`` stays total: the
        # wrapper layer sees ``response.status_code == 422`` and raises the
        # typed exception via ``_map_status_to_exception(status, response.content, ...)``,
        # which parses the envelope directly. This patch is re-applied by
        # ``scripts/sync_from_prod.py`` after every regeneration.
        d = dict(src_dict)
        _detail = d.pop("detail", UNSET)
        detail: list[ValidationError] | Unset = UNSET
        if _detail is not UNSET and isinstance(_detail, list):
            try:
                detail = [ValidationError.from_dict(item) for item in _detail]
            except (ValueError, TypeError, KeyError):
                # Items don't match the FastAPI shape — stash the raw value
                # and let the wrapper layer raise via the envelope parser.
                detail = UNSET
                d["detail"] = _detail
        elif _detail is not UNSET:
            # ``detail`` is a string / non-list — aethex envelope. Preserve
            # the raw value in additional_properties for any caller that
            # introspects ``http_validation_error["detail"]``.
            d["detail"] = _detail

        http_validation_error = cls(
            detail=detail,
        )

        http_validation_error.additional_properties = d
        return http_validation_error

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
