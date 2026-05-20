from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="TranscriptionJobResponse")


@_attrs_define
class TranscriptionJobResponse:
    """
    Attributes:
        id (str):
        created_at (None | str | Unset):
        duration_seconds (float | None | Unset):
        error_message (None | str | Unset):
        language (None | str | Unset):
        processing_time_ms (int | None | Unset):
        status (str | Unset):  Default: 'pending'.
        text (str | Unset):  Default: ''.
        updated_at (None | str | Unset):
        webhook_delivered_at (None | str | Unset):
        webhook_last_attempt_at (None | str | Unset):
        webhook_last_error (None | str | Unset):
        webhook_status (None | str | Unset):
    """

    id: str
    created_at: None | str | Unset = UNSET
    duration_seconds: float | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    processing_time_ms: int | None | Unset = UNSET
    status: str | Unset = "pending"
    text: str | Unset = ""
    updated_at: None | str | Unset = UNSET
    webhook_delivered_at: None | str | Unset = UNSET
    webhook_last_attempt_at: None | str | Unset = UNSET
    webhook_last_error: None | str | Unset = UNSET
    webhook_status: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        duration_seconds: float | None | Unset
        if isinstance(self.duration_seconds, Unset):
            duration_seconds = UNSET
        else:
            duration_seconds = self.duration_seconds

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        processing_time_ms: int | None | Unset
        if isinstance(self.processing_time_ms, Unset):
            processing_time_ms = UNSET
        else:
            processing_time_ms = self.processing_time_ms

        status = self.status

        text = self.text

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
                "id": id,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if duration_seconds is not UNSET:
            field_dict["duration_seconds"] = duration_seconds
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if language is not UNSET:
            field_dict["language"] = language
        if processing_time_ms is not UNSET:
            field_dict["processing_time_ms"] = processing_time_ms
        if status is not UNSET:
            field_dict["status"] = status
        if text is not UNSET:
            field_dict["text"] = text
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
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_duration_seconds(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        duration_seconds = _parse_duration_seconds(d.pop("duration_seconds", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        def _parse_processing_time_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        processing_time_ms = _parse_processing_time_ms(d.pop("processing_time_ms", UNSET))

        status = d.pop("status", UNSET)

        text = d.pop("text", UNSET)

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

        transcription_job_response = cls(
            id=id,
            created_at=created_at,
            duration_seconds=duration_seconds,
            error_message=error_message,
            language=language,
            processing_time_ms=processing_time_ms,
            status=status,
            text=text,
            updated_at=updated_at,
            webhook_delivered_at=webhook_delivered_at,
            webhook_last_attempt_at=webhook_last_attempt_at,
            webhook_last_error=webhook_last_error,
            webhook_status=webhook_status,
        )

        transcription_job_response.additional_properties = d
        return transcription_job_response

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
