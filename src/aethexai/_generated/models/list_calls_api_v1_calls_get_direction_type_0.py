from enum import Enum


class ListCallsApiV1CallsGetDirectionType0(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

    def __str__(self) -> str:
        return str(self.value)
