from enum import Enum


class PresignUploadRequestKind(str, Enum):
    AUDIOTRANSCRIBE = "audio/transcribe"
    DOCKNOWLEDGE_BASE = "doc/knowledge-base"

    def __str__(self) -> str:
        return str(self.value)
