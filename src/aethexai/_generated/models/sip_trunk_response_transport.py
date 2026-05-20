from enum import Enum


class SipTrunkResponseTransport(str, Enum):
    TCP = "tcp"
    TLS = "tls"
    UDP = "udp"

    def __str__(self) -> str:
        return str(self.value)
