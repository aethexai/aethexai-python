from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="DunningState")


@_attrs_define
class DunningState:
    """Payment-retry (dunning) timeline for a ``past_due`` account: how many payment retries have occurred, when the next
    retry is scheduled, when the last attempt failed, and the final cutoff after which the subscription is canceled.
    ``None`` for accounts that aren't ``past_due``. These fields let you show a banner such as "Card declined Apr 28.
    We'll retry May 1. Service stops May 19 if unresolved."

        Attributes:
            attempt_count (int | Unset): How many retries Stripe has burned on this invoice. Default: 0.
            final_cutoff_at (datetime.datetime | None | Unset): When the subscription is scheduled to be canceled if payment
                retries still fail; ``None`` if no auto-cancel is scheduled yet.
            last_failed_at (datetime.datetime | None | Unset): When Stripe last attempted the dunning charge and got
                declined.
            next_retry_at (datetime.datetime | None | Unset): When Stripe will attempt the next dunning retry. ``None`` when
                Stripe has exhausted retries (final cutoff reached).
    """

    attempt_count: int | Unset = 0
    final_cutoff_at: datetime.datetime | None | Unset = UNSET
    last_failed_at: datetime.datetime | None | Unset = UNSET
    next_retry_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempt_count = self.attempt_count

        final_cutoff_at: None | str | Unset
        if isinstance(self.final_cutoff_at, Unset):
            final_cutoff_at = UNSET
        elif isinstance(self.final_cutoff_at, datetime.datetime):
            final_cutoff_at = self.final_cutoff_at.isoformat()
        else:
            final_cutoff_at = self.final_cutoff_at

        last_failed_at: None | str | Unset
        if isinstance(self.last_failed_at, Unset):
            last_failed_at = UNSET
        elif isinstance(self.last_failed_at, datetime.datetime):
            last_failed_at = self.last_failed_at.isoformat()
        else:
            last_failed_at = self.last_failed_at

        next_retry_at: None | str | Unset
        if isinstance(self.next_retry_at, Unset):
            next_retry_at = UNSET
        elif isinstance(self.next_retry_at, datetime.datetime):
            next_retry_at = self.next_retry_at.isoformat()
        else:
            next_retry_at = self.next_retry_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attempt_count is not UNSET:
            field_dict["attempt_count"] = attempt_count
        if final_cutoff_at is not UNSET:
            field_dict["final_cutoff_at"] = final_cutoff_at
        if last_failed_at is not UNSET:
            field_dict["last_failed_at"] = last_failed_at
        if next_retry_at is not UNSET:
            field_dict["next_retry_at"] = next_retry_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attempt_count = d.pop("attempt_count", UNSET)

        def _parse_final_cutoff_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                final_cutoff_at_type_0 = isoparse(data)

                return final_cutoff_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        final_cutoff_at = _parse_final_cutoff_at(d.pop("final_cutoff_at", UNSET))

        def _parse_last_failed_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_failed_at_type_0 = isoparse(data)

                return last_failed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_failed_at = _parse_last_failed_at(d.pop("last_failed_at", UNSET))

        def _parse_next_retry_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_retry_at_type_0 = isoparse(data)

                return next_retry_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        next_retry_at = _parse_next_retry_at(d.pop("next_retry_at", UNSET))

        dunning_state = cls(
            attempt_count=attempt_count,
            final_cutoff_at=final_cutoff_at,
            last_failed_at=last_failed_at,
            next_retry_at=next_retry_at,
        )

        dunning_state.additional_properties = d
        return dunning_state

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
