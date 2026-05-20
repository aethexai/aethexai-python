from enum import Enum


class SipTrunkUpdateStatusType0(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"

    def __str__(self) -> str:
        return str(self.value)
