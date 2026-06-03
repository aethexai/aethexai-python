from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.agent_tool_update_headers_type_0 import AgentToolUpdateHeadersType0
    from ..models.agent_tool_update_parameters_schema_type_0 import (
        AgentToolUpdateParametersSchemaType0,
    )
    from ..models.agent_tool_update_parameters_type_0 import AgentToolUpdateParametersType0


T = TypeVar("T", bound="AgentToolUpdate")


@_attrs_define
class AgentToolUpdate:
    """
    Attributes:
        description (None | str | Unset):
        endpoint_url (None | str | Unset):
        headers (AgentToolUpdateHeadersType0 | None | Unset):
        name (None | str | Unset):
        parameters (AgentToolUpdateParametersType0 | None | Unset):
        parameters_schema (AgentToolUpdateParametersSchemaType0 | None | Unset):
        tool_type (None | str | Unset):
    """

    description: None | str | Unset = UNSET
    endpoint_url: None | str | Unset = UNSET
    headers: AgentToolUpdateHeadersType0 | None | Unset = UNSET
    name: None | str | Unset = UNSET
    parameters: AgentToolUpdateParametersType0 | None | Unset = UNSET
    parameters_schema: AgentToolUpdateParametersSchemaType0 | None | Unset = UNSET
    tool_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_tool_update_headers_type_0 import AgentToolUpdateHeadersType0
        from ..models.agent_tool_update_parameters_schema_type_0 import (
            AgentToolUpdateParametersSchemaType0,
        )
        from ..models.agent_tool_update_parameters_type_0 import AgentToolUpdateParametersType0

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        endpoint_url: None | str | Unset
        if isinstance(self.endpoint_url, Unset):
            endpoint_url = UNSET
        else:
            endpoint_url = self.endpoint_url

        headers: dict[str, Any] | None | Unset
        if isinstance(self.headers, Unset):
            headers = UNSET
        elif isinstance(self.headers, AgentToolUpdateHeadersType0):
            headers = self.headers.to_dict()
        else:
            headers = self.headers

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        parameters: dict[str, Any] | None | Unset
        if isinstance(self.parameters, Unset):
            parameters = UNSET
        elif isinstance(self.parameters, AgentToolUpdateParametersType0):
            parameters = self.parameters.to_dict()
        else:
            parameters = self.parameters

        parameters_schema: dict[str, Any] | None | Unset
        if isinstance(self.parameters_schema, Unset):
            parameters_schema = UNSET
        elif isinstance(self.parameters_schema, AgentToolUpdateParametersSchemaType0):
            parameters_schema = self.parameters_schema.to_dict()
        else:
            parameters_schema = self.parameters_schema

        tool_type: None | str | Unset
        if isinstance(self.tool_type, Unset):
            tool_type = UNSET
        else:
            tool_type = self.tool_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if endpoint_url is not UNSET:
            field_dict["endpoint_url"] = endpoint_url
        if headers is not UNSET:
            field_dict["headers"] = headers
        if name is not UNSET:
            field_dict["name"] = name
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if parameters_schema is not UNSET:
            field_dict["parameters_schema"] = parameters_schema
        if tool_type is not UNSET:
            field_dict["tool_type"] = tool_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_tool_update_headers_type_0 import AgentToolUpdateHeadersType0
        from ..models.agent_tool_update_parameters_schema_type_0 import (
            AgentToolUpdateParametersSchemaType0,
        )
        from ..models.agent_tool_update_parameters_type_0 import AgentToolUpdateParametersType0

        d = dict(src_dict)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_endpoint_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        endpoint_url = _parse_endpoint_url(d.pop("endpoint_url", UNSET))

        def _parse_headers(data: object) -> AgentToolUpdateHeadersType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                headers_type_0 = AgentToolUpdateHeadersType0.from_dict(data)

                return headers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgentToolUpdateHeadersType0 | None | Unset, data)

        headers = _parse_headers(d.pop("headers", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_parameters(data: object) -> AgentToolUpdateParametersType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parameters_type_0 = AgentToolUpdateParametersType0.from_dict(data)

                return parameters_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgentToolUpdateParametersType0 | None | Unset, data)

        parameters = _parse_parameters(d.pop("parameters", UNSET))

        def _parse_parameters_schema(
            data: object,
        ) -> AgentToolUpdateParametersSchemaType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parameters_schema_type_0 = AgentToolUpdateParametersSchemaType0.from_dict(data)

                return parameters_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgentToolUpdateParametersSchemaType0 | None | Unset, data)

        parameters_schema = _parse_parameters_schema(d.pop("parameters_schema", UNSET))

        def _parse_tool_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tool_type = _parse_tool_type(d.pop("tool_type", UNSET))

        agent_tool_update = cls(
            description=description,
            endpoint_url=endpoint_url,
            headers=headers,
            name=name,
            parameters=parameters,
            parameters_schema=parameters_schema,
            tool_type=tool_type,
        )

        agent_tool_update.additional_properties = d
        return agent_tool_update

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
