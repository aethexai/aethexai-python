from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.transaction_entry import TransactionEntry


T = TypeVar("T", bound="TransactionListResponse")


@_attrs_define
class TransactionListResponse:
    """``GET /billing/transactions`` payload. Cursor pagination so the
    portal can scroll through arbitrarily large ledgers without offset
    pathologies on hot tenants. Clients pass ``next_cursor`` back as ``?cursor=...`` (the canonical
    request param). ``?next_cursor=...`` is also accepted for clients
    that intuitively echo the response field name. When ``next_cursor``
    is null the caller has reached the oldest entry. The response field is named ``next_cursor`` (not ``cursor``) and
    must
    stay that way: the portal and SDK consumers have typed against it. Only the *request* surface accepts both names.

        Attributes:
            transactions (list[TransactionEntry]):
            next_cursor (None | str | Unset):
    """

    transactions: list[TransactionEntry]
    next_cursor: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.transaction_entry import TransactionEntry

        transactions = []
        for transactions_item_data in self.transactions:
            transactions_item = transactions_item_data.to_dict()
            transactions.append(transactions_item)

        next_cursor: None | str | Unset
        if isinstance(self.next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transactions": transactions,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transaction_entry import TransactionEntry

        d = dict(src_dict)
        transactions = []
        _transactions = d.pop("transactions")
        for transactions_item_data in _transactions:
            transactions_item = TransactionEntry.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        def _parse_next_cursor(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor", UNSET))

        transaction_list_response = cls(
            transactions=transactions,
            next_cursor=next_cursor,
        )

        transaction_list_response.additional_properties = d
        return transaction_list_response

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
