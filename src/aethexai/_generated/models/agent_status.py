from enum import Enum


class AgentStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"

    def __str__(self) -> str:
        return str(self.value)
