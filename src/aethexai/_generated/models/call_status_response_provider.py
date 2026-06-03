from enum import Enum


class CallStatusResponseProvider(str, Enum):
    AETHEX_SIP = "aethex-sip"
    SIP = "sip"
    TWILIO = "twilio"
    WEBRTC = "webrtc"

    def __str__(self) -> str:
        return str(self.value)
