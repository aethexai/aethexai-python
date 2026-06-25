from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.plan_catalog_entry import PlanCatalogEntry


T = TypeVar("T", bound="PlanListResponse")


@_attrs_define
class PlanListResponse:
    """Payload for ``GET /billing/plans``: the catalogue of selectable plans plus ``current_plan_slug`` so a plan picker can highlight the tenant's current tier without a second ``/billing/balance`` call.

        Attributes:
            current_plan_slug (str):
            plans (list[PlanCatalogEntry]):
    """

    current_plan_slug: str
    plans: list[PlanCatalogEntry]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.plan_catalog_entry import PlanCatalogEntry

        current_plan_slug = self.current_plan_slug

        plans = []
        for plans_item_data in self.plans:
            plans_item = plans_item_data.to_dict()
            plans.append(plans_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_plan_slug": current_plan_slug,
                "plans": plans,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plan_catalog_entry import PlanCatalogEntry

        d = dict(src_dict)
        current_plan_slug = d.pop("current_plan_slug")

        plans = []
        _plans = d.pop("plans")
        for plans_item_data in _plans:
            plans_item = PlanCatalogEntry.from_dict(plans_item_data)

            plans.append(plans_item)

        plan_list_response = cls(
            current_plan_slug=current_plan_slug,
            plans=plans,
        )

        plan_list_response.additional_properties = d
        return plan_list_response

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
