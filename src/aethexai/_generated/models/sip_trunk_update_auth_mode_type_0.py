from enum import Enum


class SipTrunkUpdateAuthModeType0(str, Enum):
    DIGEST = "digest"
    DIGEST_PLUS_IP_ACL = "digest_plus_ip_acl"
    IP_ACL = "ip_acl"

    def __str__(self) -> str:
        return str(self.value)
