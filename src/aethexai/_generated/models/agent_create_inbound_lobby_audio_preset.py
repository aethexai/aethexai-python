from enum import Enum


class AgentCreateInboundLobbyAudioPreset(str, Enum):
    AMBIENT = "ambient"
    INSTRUMENTAL = "instrumental"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
