from enum import Enum


class PaymentMethodSummaryType(str, Enum):
    CARD = "card"
    LINK = "link"

    def __str__(self) -> str:
        return str(self.value)
