from enum import Enum


class VoiceMetadataUpdateStatusType0(str, Enum):
    ACTIVE = "active"
    RETIRED = "retired"

    def __str__(self) -> str:
        return str(self.value)
