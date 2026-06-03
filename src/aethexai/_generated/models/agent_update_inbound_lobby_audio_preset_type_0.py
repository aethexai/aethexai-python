from enum import Enum


class AgentUpdateInboundLobbyAudioPresetType0(str, Enum):
    AMBIENT = "ambient"
    INSTRUMENTAL = "instrumental"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
