from enum import Enum


class SipTrunkResponseMediaEncryption(str, Enum):
    ALLOW = "allow"
    DISABLE = "disable"
    REQUIRE = "require"

    def __str__(self) -> str:
        return str(self.value)
