from enum import Enum


class ModelEntryProvider(str, Enum):
    AETHEX = "aethex"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"
    OPENAI = "openai"
    XAI = "xai"

    def __str__(self) -> str:
        return str(self.value)
