from enum import Enum


class ListCallsApiV1CallsGetStatusType0(str, Enum):
    BUSY = "busy"
    CANCELED = "canceled"
    COMPLETED = "completed"
    FAILED = "failed"
    IN_PROGRESS = "in-progress"
    NO_ANSWER = "no-answer"
    QUEUED = "queued"
    RINGING = "ringing"

    def __str__(self) -> str:
        return str(self.value)
