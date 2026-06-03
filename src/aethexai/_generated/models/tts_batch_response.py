from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.tts_batch_item_result import TTSBatchItemResult


T = TypeVar("T", bound="TTSBatchResponse")


@_attrs_define
class TTSBatchResponse:
    """
    Attributes:
        batch_id (str):
        completed (int):
        failed (int):
        status (str):
        total (int):
        created_at (None | str | Unset):
        results (list[TTSBatchItemResult] | Unset):
        updated_at (None | str | Unset):
        webhook_delivered_at (None | str | Unset):
        webhook_last_attempt_at (None | str | Unset):
        webhook_last_error (None | str | Unset):
        webhook_status (None | str | Unset):
    """

    batch_id: str
    completed: int
    failed: int
    status: str
    total: int
    created_at: None | str | Unset = UNSET
    results: list[TTSBatchItemResult] | Unset = UNSET
    updated_at: None | str | Unset = UNSET
    webhook_delivered_at: None | str | Unset = UNSET
    webhook_last_attempt_at: None | str | Unset = UNSET
    webhook_last_error: None | str | Unset = UNSET
    webhook_status: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.tts_batch_item_result import TTSBatchItemResult

        batch_id = self.batch_id

        completed = self.completed

        failed = self.failed

        status = self.status

        total = self.total

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        results: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = self.updated_at

        webhook_delivered_at: None | str | Unset
        if isinstance(self.webhook_delivered_at, Unset):
            webhook_delivered_at = UNSET
        else:
            webhook_delivered_at = self.webhook_delivered_at

        webhook_last_attempt_at: None | str | Unset
        if isinstance(self.webhook_last_attempt_at, Unset):
            webhook_last_attempt_at = UNSET
        else:
            webhook_last_attempt_at = self.webhook_last_attempt_at

        webhook_last_error: None | str | Unset
        if isinstance(self.webhook_last_error, Unset):
            webhook_last_error = UNSET
        else:
            webhook_last_error = self.webhook_last_error

        webhook_status: None | str | Unset
        if isinstance(self.webhook_status, Unset):
            webhook_status = UNSET
        else:
            webhook_status = self.webhook_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "batch_id": batch_id,
                "completed": completed,
                "failed": failed,
                "status": status,
                "total": total,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if results is not UNSET:
            field_dict["results"] = results
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if webhook_delivered_at is not UNSET:
            field_dict["webhook_delivered_at"] = webhook_delivered_at
        if webhook_last_attempt_at is not UNSET:
            field_dict["webhook_last_attempt_at"] = webhook_last_attempt_at
        if webhook_last_error is not UNSET:
            field_dict["webhook_last_error"] = webhook_last_error
        if webhook_status is not UNSET:
            field_dict["webhook_status"] = webhook_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tts_batch_item_result import TTSBatchItemResult

        d = dict(src_dict)
        batch_id = d.pop("batch_id")

        completed = d.pop("completed")

        failed = d.pop("failed")

        status = d.pop("status")

        total = d.pop("total")

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        _results = d.pop("results", UNSET)
        results: list[TTSBatchItemResult] | Unset = UNSET
        if _results is not UNSET:
            results = []
            for results_item_data in _results:
                results_item = TTSBatchItemResult.from_dict(results_item_data)

                results.append(results_item)

        def _parse_updated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_webhook_delivered_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        webhook_delivered_at = _parse_webhook_delivered_at(d.pop("webhook_delivered_at", UNSET))

        def _parse_webhook_last_attempt_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        webhook_last_attempt_at = _parse_webhook_last_attempt_at(
            d.pop("webhook_last_attempt_at", UNSET)
        )

        def _parse_webhook_last_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        webhook_last_error = _parse_webhook_last_error(d.pop("webhook_last_error", UNSET))

        def _parse_webhook_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        webhook_status = _parse_webhook_status(d.pop("webhook_status", UNSET))

        tts_batch_response = cls(
            batch_id=batch_id,
            completed=completed,
            failed=failed,
            status=status,
            total=total,
            created_at=created_at,
            results=results,
            updated_at=updated_at,
            webhook_delivered_at=webhook_delivered_at,
            webhook_last_attempt_at=webhook_last_attempt_at,
            webhook_last_error=webhook_last_error,
            webhook_status=webhook_status,
        )

        tts_batch_response.additional_properties = d
        return tts_batch_response

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
