from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.agent_tool_create_headers_type_0 import AgentToolCreateHeadersType0
    from ..models.agent_tool_create_parameters_schema import AgentToolCreateParametersSchema
    from ..models.agent_tool_create_parameters_type_0 import AgentToolCreateParametersType0


T = TypeVar("T", bound="AgentToolCreate")


@_attrs_define
class AgentToolCreate:
    """
    Attributes:
        name (str):
        description (str | Unset):  Default: ''.
        endpoint_url (None | str | Unset):
        headers (AgentToolCreateHeadersType0 | None | Unset):
        parameters (AgentToolCreateParametersType0 | None | Unset):
        parameters_schema (AgentToolCreateParametersSchema | Unset):
        tool_type (str | Unset):  Default: 'function'.
    """

    name: str
    description: str | Unset = ""
    endpoint_url: None | str | Unset = UNSET
    headers: AgentToolCreateHeadersType0 | None | Unset = UNSET
    parameters: AgentToolCreateParametersType0 | None | Unset = UNSET
    parameters_schema: AgentToolCreateParametersSchema | Unset = UNSET
    tool_type: str | Unset = "function"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_tool_create_headers_type_0 import AgentToolCreateHeadersType0
        from ..models.agent_tool_create_parameters_schema import AgentToolCreateParametersSchema
        from ..models.agent_tool_create_parameters_type_0 import AgentToolCreateParametersType0

        name = self.name

        description = self.description

        endpoint_url: None | str | Unset
        if isinstance(self.endpoint_url, Unset):
            endpoint_url = UNSET
        else:
            endpoint_url = self.endpoint_url

        headers: dict[str, Any] | None | Unset
        if isinstance(self.headers, Unset):
            headers = UNSET
        elif isinstance(self.headers, AgentToolCreateHeadersType0):
            headers = self.headers.to_dict()
        else:
            headers = self.headers

        parameters: dict[str, Any] | None | Unset
        if isinstance(self.parameters, Unset):
            parameters = UNSET
        elif isinstance(self.parameters, AgentToolCreateParametersType0):
            parameters = self.parameters.to_dict()
        else:
            parameters = self.parameters

        parameters_schema: dict[str, Any] | Unset = UNSET
        if not isinstance(self.parameters_schema, Unset):
            parameters_schema = self.parameters_schema.to_dict()

        tool_type = self.tool_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if endpoint_url is not UNSET:
            field_dict["endpoint_url"] = endpoint_url
        if headers is not UNSET:
            field_dict["headers"] = headers
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if parameters_schema is not UNSET:
            field_dict["parameters_schema"] = parameters_schema
        if tool_type is not UNSET:
            field_dict["tool_type"] = tool_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_tool_create_headers_type_0 import AgentToolCreateHeadersType0
        from ..models.agent_tool_create_parameters_schema import AgentToolCreateParametersSchema
        from ..models.agent_tool_create_parameters_type_0 import AgentToolCreateParametersType0

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        def _parse_endpoint_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        endpoint_url = _parse_endpoint_url(d.pop("endpoint_url", UNSET))

        def _parse_headers(data: object) -> AgentToolCreateHeadersType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                headers_type_0 = AgentToolCreateHeadersType0.from_dict(data)

                return headers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgentToolCreateHeadersType0 | None | Unset, data)

        headers = _parse_headers(d.pop("headers", UNSET))

        def _parse_parameters(data: object) -> AgentToolCreateParametersType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parameters_type_0 = AgentToolCreateParametersType0.from_dict(data)

                return parameters_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgentToolCreateParametersType0 | None | Unset, data)

        parameters = _parse_parameters(d.pop("parameters", UNSET))

        _parameters_schema = d.pop("parameters_schema", UNSET)
        parameters_schema: AgentToolCreateParametersSchema | Unset
        if isinstance(_parameters_schema, Unset):
            parameters_schema = UNSET
        else:
            parameters_schema = AgentToolCreateParametersSchema.from_dict(_parameters_schema)

        tool_type = d.pop("tool_type", UNSET)

        agent_tool_create = cls(
            name=name,
            description=description,
            endpoint_url=endpoint_url,
            headers=headers,
            parameters=parameters,
            parameters_schema=parameters_schema,
            tool_type=tool_type,
        )

        agent_tool_create.additional_properties = d
        return agent_tool_create

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
