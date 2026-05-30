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

if TYPE_CHECKING:
    from ..models.usage_trigger_firing_response_payload import UsageTriggerFiringResponsePayload


T = TypeVar("T", bound="UsageTriggerFiringResponse")


@_attrs_define
class UsageTriggerFiringResponse:
    """One row from ``GET /usage/triggers/{id}/firings``. ``payload`` is the exact JSON we POSTed to the customer's URL so
    they
    can replay it against their handler when debugging a missed event. ``delivery_status`` reflects the final state
    after retries:
    ``delivered`` / ``failed`` / ``pending``.

        Attributes:
            delivery_status (str):
            fired_at (datetime.datetime):
            id (str):
            observed_value (str):
            period_ends_at (datetime.datetime):
            period_started_at (datetime.datetime):
            threshold_value (str):
            attempt_count (int | Unset):  Default: 0.
            http_status (int | None | Unset):
            last_error (None | str | Unset):
            payload (UsageTriggerFiringResponsePayload | Unset):
    """

    delivery_status: str
    fired_at: datetime.datetime
    id: str
    observed_value: str
    period_ends_at: datetime.datetime
    period_started_at: datetime.datetime
    threshold_value: str
    attempt_count: int | Unset = 0
    http_status: int | None | Unset = UNSET
    last_error: None | str | Unset = UNSET
    payload: UsageTriggerFiringResponsePayload | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_trigger_firing_response_payload import UsageTriggerFiringResponsePayload

        delivery_status = self.delivery_status

        fired_at = self.fired_at.isoformat()

        id = self.id

        observed_value = self.observed_value

        period_ends_at = self.period_ends_at.isoformat()

        period_started_at = self.period_started_at.isoformat()

        threshold_value = self.threshold_value

        attempt_count = self.attempt_count

        http_status: int | None | Unset
        if isinstance(self.http_status, Unset):
            http_status = UNSET
        else:
            http_status = self.http_status

        last_error: None | str | Unset
        if isinstance(self.last_error, Unset):
            last_error = UNSET
        else:
            last_error = self.last_error

        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "delivery_status": delivery_status,
                "fired_at": fired_at,
                "id": id,
                "observed_value": observed_value,
                "period_ends_at": period_ends_at,
                "period_started_at": period_started_at,
                "threshold_value": threshold_value,
            }
        )
        if attempt_count is not UNSET:
            field_dict["attempt_count"] = attempt_count
        if http_status is not UNSET:
            field_dict["http_status"] = http_status
        if last_error is not UNSET:
            field_dict["last_error"] = last_error
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_trigger_firing_response_payload import UsageTriggerFiringResponsePayload

        d = dict(src_dict)
        delivery_status = d.pop("delivery_status")

        fired_at = isoparse(d.pop("fired_at"))

        id = d.pop("id")

        observed_value = d.pop("observed_value")

        period_ends_at = isoparse(d.pop("period_ends_at"))

        period_started_at = isoparse(d.pop("period_started_at"))

        threshold_value = d.pop("threshold_value")

        attempt_count = d.pop("attempt_count", UNSET)

        def _parse_http_status(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        http_status = _parse_http_status(d.pop("http_status", UNSET))

        def _parse_last_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_error = _parse_last_error(d.pop("last_error", UNSET))

        _payload = d.pop("payload", UNSET)
        payload: UsageTriggerFiringResponsePayload | Unset
        if isinstance(_payload, Unset):
            payload = UNSET
        else:
            payload = UsageTriggerFiringResponsePayload.from_dict(_payload)

        usage_trigger_firing_response = cls(
            delivery_status=delivery_status,
            fired_at=fired_at,
            id=id,
            observed_value=observed_value,
            period_ends_at=period_ends_at,
            period_started_at=period_started_at,
            threshold_value=threshold_value,
            attempt_count=attempt_count,
            http_status=http_status,
            last_error=last_error,
            payload=payload,
        )

        usage_trigger_firing_response.additional_properties = d
        return usage_trigger_firing_response

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
