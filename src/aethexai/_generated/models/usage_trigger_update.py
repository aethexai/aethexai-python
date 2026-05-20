from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="UsageTriggerUpdate")


@_attrs_define
class UsageTriggerUpdate:
    """Partial update for ``PATCH /usage/triggers/{id}``.

    Only fields a customer can re-tune in place are exposed: the
    ``is_active`` flag (deactivate to recover the per-tenant cap
    without losing audit history), the threshold value (re-tune the
    trip point as their volume scales), and the callback URL (rotate
    the receiver). The trigger's *shape* — ``resource_type``,
    ``threshold_type``, ``period`` — is immutable; a different shape
    is logically a different trigger and should be created fresh so
    the firings audit table cleanly tracks one configuration over
    time.

    Every field is Optional; PATCH is partial. An empty body is a
    valid no-op.

    ``extra='forbid'`` rejects unknown keys with HTTP 422. This catches
    two real customer foot-guns at once: PATCHing an immutable shape
    field (``resource_type`` / ``threshold_type`` / ``period``) used
    to return 200 with the value silently dropped, and a misspelled
    editable field name (e.g. ``threshold_val``) used to return 200
    with no clue the change was ignored. Both now surface as an
    explicit validation error at the boundary.

        Attributes:
            event_callback_url (None | str | Unset):
            is_active (bool | None | Unset):
            threshold_value (float | None | str | Unset):
    """

    event_callback_url: None | str | Unset = UNSET
    is_active: bool | None | Unset = UNSET
    threshold_value: float | None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        event_callback_url: None | str | Unset
        if isinstance(self.event_callback_url, Unset):
            event_callback_url = UNSET
        else:
            event_callback_url = self.event_callback_url

        is_active: bool | None | Unset
        if isinstance(self.is_active, Unset):
            is_active = UNSET
        else:
            is_active = self.is_active

        threshold_value: float | None | str | Unset
        if isinstance(self.threshold_value, Unset):
            threshold_value = UNSET
        else:
            threshold_value = self.threshold_value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if event_callback_url is not UNSET:
            field_dict["event_callback_url"] = event_callback_url
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if threshold_value is not UNSET:
            field_dict["threshold_value"] = threshold_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_event_callback_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        event_callback_url = _parse_event_callback_url(d.pop("event_callback_url", UNSET))

        def _parse_is_active(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_active = _parse_is_active(d.pop("is_active", UNSET))

        def _parse_threshold_value(data: object) -> float | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | str | Unset, data)

        threshold_value = _parse_threshold_value(d.pop("threshold_value", UNSET))

        usage_trigger_update = cls(
            event_callback_url=event_callback_url,
            is_active=is_active,
            threshold_value=threshold_value,
        )

        return usage_trigger_update
