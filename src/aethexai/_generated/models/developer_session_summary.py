from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="DeveloperSessionSummary")


@_attrs_define
class DeveloperSessionSummary:
    """A single active session returned by ``GET /auth/sessions`` for the "where you're signed in" view. ``id`` is a short
    opaque identifier safe to display; it is not a session credential. ``created_ip``, ``last_activity_ip``, and
    ``user_agent`` are best-effort and may be null.

        Attributes:
            absolute_expires_at (None | str):
            created_at (None | str):
            created_ip (None | str):
            id (str):
            idle_expires_at (None | str):
            is_current (bool):
            last_activity_at (None | str):
            last_activity_ip (None | str):
            user_agent (None | str):
    """

    absolute_expires_at: None | str
    created_at: None | str
    created_ip: None | str
    id: str
    idle_expires_at: None | str
    is_current: bool
    last_activity_at: None | str
    last_activity_ip: None | str
    user_agent: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        absolute_expires_at: None | str
        absolute_expires_at = self.absolute_expires_at

        created_at: None | str
        created_at = self.created_at

        created_ip: None | str
        created_ip = self.created_ip

        id = self.id

        idle_expires_at: None | str
        idle_expires_at = self.idle_expires_at

        is_current = self.is_current

        last_activity_at: None | str
        last_activity_at = self.last_activity_at

        last_activity_ip: None | str
        last_activity_ip = self.last_activity_ip

        user_agent: None | str
        user_agent = self.user_agent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "absolute_expires_at": absolute_expires_at,
                "created_at": created_at,
                "created_ip": created_ip,
                "id": id,
                "idle_expires_at": idle_expires_at,
                "is_current": is_current,
                "last_activity_at": last_activity_at,
                "last_activity_ip": last_activity_ip,
                "user_agent": user_agent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_absolute_expires_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        absolute_expires_at = _parse_absolute_expires_at(d.pop("absolute_expires_at"))

        def _parse_created_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        created_at = _parse_created_at(d.pop("created_at"))

        def _parse_created_ip(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        created_ip = _parse_created_ip(d.pop("created_ip"))

        id = d.pop("id")

        def _parse_idle_expires_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        idle_expires_at = _parse_idle_expires_at(d.pop("idle_expires_at"))

        is_current = d.pop("is_current")

        def _parse_last_activity_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_activity_at = _parse_last_activity_at(d.pop("last_activity_at"))

        def _parse_last_activity_ip(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_activity_ip = _parse_last_activity_ip(d.pop("last_activity_ip"))

        def _parse_user_agent(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        user_agent = _parse_user_agent(d.pop("user_agent"))

        developer_session_summary = cls(
            absolute_expires_at=absolute_expires_at,
            created_at=created_at,
            created_ip=created_ip,
            id=id,
            idle_expires_at=idle_expires_at,
            is_current=is_current,
            last_activity_at=last_activity_at,
            last_activity_ip=last_activity_ip,
            user_agent=user_agent,
        )

        developer_session_summary.additional_properties = d
        return developer_session_summary

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
