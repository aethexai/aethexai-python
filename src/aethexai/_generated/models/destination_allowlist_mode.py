from enum import Enum


class DestinationAllowlistMode(str, Enum):
    ALLOWLIST = "allowlist"
    BLOCKLIST = "blocklist"

    def __str__(self) -> str:
        return str(self.value)
