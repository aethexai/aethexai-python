from enum import Enum


class SipTrunkOnboardRequestMediaEncryption(str, Enum):
    ALLOW = "allow"
    DISABLE = "disable"
    REQUIRE = "require"

    def __str__(self) -> str:
        return str(self.value)
