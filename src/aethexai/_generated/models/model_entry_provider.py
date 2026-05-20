from enum import Enum


class ModelEntryProvider(str, Enum):
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    OPENAI = "openai"
    OPENROUTER = "openrouter"

    def __str__(self) -> str:
        return str(self.value)
