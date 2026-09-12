from typing import Optional


class CreditCardMockError(Exception):
    """Base exception class for the mock credit-card server."""

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(CreditCardMockError):
    code = "BAD_ARG"


class CardNotFoundError(CreditCardMockError):
    code = "CARD_NOT_FOUND"


class CardFrozenError(CreditCardMockError):
    code = "CARD_FROZEN"


class OverLimitError(CreditCardMockError):
    code = "OVER_LIMIT"


class OverpaymentError(CreditCardMockError):
    code = "OVERPAYMENT"


class InvalidAmountError(CreditCardMockError):
    code = "INVALID_AMOUNT"


class DisputeAlreadyOpenError(CreditCardMockError):
    code = "DISPUTE_ALREADY_OPEN"


class TransactionNotFoundError(CreditCardMockError):
    code = "TX_NOT_FOUND"


class StatementNotFoundError(CreditCardMockError):
    code = "STATEMENT_NOT_FOUND"


class InsufficientPointsError(CreditCardMockError):
    code = "INSUFFICIENT_POINTS"


class BadRedemptionError(CreditCardMockError):
    code = "BAD_REDEMPTION"
