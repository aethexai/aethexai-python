from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="InvoiceEntry")


@_attrs_define
class InvoiceEntry:
    """A single invoice in the customer's billing history. Sourced
    directly from Stripe; no PDF rendering on our side. The portal
    table renders ``hosted_invoice_url`` as "View" and ``invoice_pdf``
    as "Download PDF" links that 302 to Stripe-hosted assets.

    ``status`` is one of ``draft / open / paid / uncollectible / void``.
    ``amount_paid`` and ``amount_due`` are USD cents. ``created`` /
    ``period_start`` / ``period_end`` are Unix epochs (seconds) so the
    portal can render whatever timezone-local format the user expects
    without us forcing a representation here.

    ``hosted_invoice_url`` and ``invoice_pdf`` can be ``None`` for
    invoices in the ``draft`` state (no PDF generated yet).

        Attributes:
            id (str):
            amount_due (int | None | Unset):
            amount_paid (int | None | Unset):
            created (int | None | Unset):
            currency (None | str | Unset):
            hosted_invoice_url (None | str | Unset):
            invoice_pdf (None | str | Unset):
            number (None | str | Unset):
            period_end (int | None | Unset):
            period_start (int | None | Unset):
            status (None | str | Unset):
            subscription (None | str | Unset):
    """

    id: str
    amount_due: int | None | Unset = UNSET
    amount_paid: int | None | Unset = UNSET
    created: int | None | Unset = UNSET
    currency: None | str | Unset = UNSET
    hosted_invoice_url: None | str | Unset = UNSET
    invoice_pdf: None | str | Unset = UNSET
    number: None | str | Unset = UNSET
    period_end: int | None | Unset = UNSET
    period_start: int | None | Unset = UNSET
    status: None | str | Unset = UNSET
    subscription: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        amount_due: int | None | Unset
        if isinstance(self.amount_due, Unset):
            amount_due = UNSET
        else:
            amount_due = self.amount_due

        amount_paid: int | None | Unset
        if isinstance(self.amount_paid, Unset):
            amount_paid = UNSET
        else:
            amount_paid = self.amount_paid

        created: int | None | Unset
        if isinstance(self.created, Unset):
            created = UNSET
        else:
            created = self.created

        currency: None | str | Unset
        if isinstance(self.currency, Unset):
            currency = UNSET
        else:
            currency = self.currency

        hosted_invoice_url: None | str | Unset
        if isinstance(self.hosted_invoice_url, Unset):
            hosted_invoice_url = UNSET
        else:
            hosted_invoice_url = self.hosted_invoice_url

        invoice_pdf: None | str | Unset
        if isinstance(self.invoice_pdf, Unset):
            invoice_pdf = UNSET
        else:
            invoice_pdf = self.invoice_pdf

        number: None | str | Unset
        if isinstance(self.number, Unset):
            number = UNSET
        else:
            number = self.number

        period_end: int | None | Unset
        if isinstance(self.period_end, Unset):
            period_end = UNSET
        else:
            period_end = self.period_end

        period_start: int | None | Unset
        if isinstance(self.period_start, Unset):
            period_start = UNSET
        else:
            period_start = self.period_start

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        subscription: None | str | Unset
        if isinstance(self.subscription, Unset):
            subscription = UNSET
        else:
            subscription = self.subscription

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if amount_due is not UNSET:
            field_dict["amount_due"] = amount_due
        if amount_paid is not UNSET:
            field_dict["amount_paid"] = amount_paid
        if created is not UNSET:
            field_dict["created"] = created
        if currency is not UNSET:
            field_dict["currency"] = currency
        if hosted_invoice_url is not UNSET:
            field_dict["hosted_invoice_url"] = hosted_invoice_url
        if invoice_pdf is not UNSET:
            field_dict["invoice_pdf"] = invoice_pdf
        if number is not UNSET:
            field_dict["number"] = number
        if period_end is not UNSET:
            field_dict["period_end"] = period_end
        if period_start is not UNSET:
            field_dict["period_start"] = period_start
        if status is not UNSET:
            field_dict["status"] = status
        if subscription is not UNSET:
            field_dict["subscription"] = subscription

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_amount_due(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        amount_due = _parse_amount_due(d.pop("amount_due", UNSET))

        def _parse_amount_paid(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        amount_paid = _parse_amount_paid(d.pop("amount_paid", UNSET))

        def _parse_created(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        created = _parse_created(d.pop("created", UNSET))

        def _parse_currency(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        currency = _parse_currency(d.pop("currency", UNSET))

        def _parse_hosted_invoice_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        hosted_invoice_url = _parse_hosted_invoice_url(d.pop("hosted_invoice_url", UNSET))

        def _parse_invoice_pdf(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        invoice_pdf = _parse_invoice_pdf(d.pop("invoice_pdf", UNSET))

        def _parse_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        number = _parse_number(d.pop("number", UNSET))

        def _parse_period_end(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        period_end = _parse_period_end(d.pop("period_end", UNSET))

        def _parse_period_start(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        period_start = _parse_period_start(d.pop("period_start", UNSET))

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_subscription(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        subscription = _parse_subscription(d.pop("subscription", UNSET))

        invoice_entry = cls(
            id=id,
            amount_due=amount_due,
            amount_paid=amount_paid,
            created=created,
            currency=currency,
            hosted_invoice_url=hosted_invoice_url,
            invoice_pdf=invoice_pdf,
            number=number,
            period_end=period_end,
            period_start=period_start,
            status=status,
            subscription=subscription,
        )

        invoice_entry.additional_properties = d
        return invoice_entry

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
