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
    from ..models.transaction_entry_details import TransactionEntryDetails


T = TypeVar("T", bound="TransactionEntry")


@_attrs_define
class TransactionEntry:
    """A single ledger row, surfaced to the portal transactions page.

    ``details`` is the row's metadata column passed through opaquely; the
    portal can render whatever it finds (call_id, tts_chars, asr_seconds,
    Stripe payment_intent_id) without us promising a stable shape.

        Attributes:
            amount (str): Signed credit movement: negative for usage / charges, positive for grants / top-ups.
            balance_after (str): Tenant balance after this entry was applied.
            created_at (datetime.datetime):
            id (str):
            tx_type (str):
            details (TransactionEntryDetails | Unset): Free-form metadata (call_id, resource counts, idempotency key, etc).
                Shape is not guaranteed and may change per tx_type.
    """

    amount: str
    balance_after: str
    created_at: datetime.datetime
    id: str
    tx_type: str
    details: TransactionEntryDetails | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.transaction_entry_details import TransactionEntryDetails

        amount = self.amount

        balance_after = self.balance_after

        created_at = self.created_at.isoformat()

        id = self.id

        tx_type = self.tx_type

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "balance_after": balance_after,
                "created_at": created_at,
                "id": id,
                "tx_type": tx_type,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transaction_entry_details import TransactionEntryDetails

        d = dict(src_dict)
        amount = d.pop("amount")

        balance_after = d.pop("balance_after")

        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        tx_type = d.pop("tx_type")

        _details = d.pop("details", UNSET)
        details: TransactionEntryDetails | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = TransactionEntryDetails.from_dict(_details)

        transaction_entry = cls(
            amount=amount,
            balance_after=balance_after,
            created_at=created_at,
            id=id,
            tx_type=tx_type,
            details=details,
        )

        transaction_entry.additional_properties = d
        return transaction_entry

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
