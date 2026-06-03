from enum import Enum


class InboundRoutingConfigFallbackAction(str, Enum):
    FORWARD = "forward"
    HANGUP = "hangup"
    VOICEMAIL = "voicemail"

    def __str__(self) -> str:
        return str(self.value)
