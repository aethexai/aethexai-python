from enum import Enum


class SipTrunkOnboardRequestTransport(str, Enum):
    TCP = "tcp"
    TLS = "tls"
    UDP = "udp"

    def __str__(self) -> str:
        return str(self.value)
