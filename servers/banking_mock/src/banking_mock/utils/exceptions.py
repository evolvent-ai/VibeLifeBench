from typing import Optional


class BankingMockError(Exception):
    """Base exception for the banking mock server.

    Mapped to ``{"error": ..., "code": ...}`` JSON by the tool decorator;
    never raised across the MCP boundary.
    """

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(BankingMockError):
    code = "BAD_ARG"


class BadAmountError(BankingMockError):
    code = "BAD_AMOUNT"


class BadDateError(BankingMockError):
    code = "BAD_DATE"


class BadFreqError(BankingMockError):
    code = "BAD_FREQ"


class AccountNotFoundError(BankingMockError):
    code = "ACCOUNT_NOT_FOUND"


class AccountFrozenError(BankingMockError):
    code = "ACCOUNT_FROZEN"


class InsufficientFundsError(BankingMockError):
    code = "INSUFFICIENT_FUNDS"


class PayeeNotFoundError(BankingMockError):
    code = "PAYEE_NOT_FOUND"


class ScheduleNotFoundError(BankingMockError):
    code = "SCHEDULE_NOT_FOUND"


class CrossUserTransferError(BankingMockError):
    code = "CROSS_USER_TRANSFER"
