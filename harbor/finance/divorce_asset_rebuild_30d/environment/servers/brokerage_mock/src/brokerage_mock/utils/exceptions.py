"""Stable error codes for brokerage_mock.

Every code here is documented in SPEC.md Appendix A and is part of the
public tool contract.
"""
from typing import Optional


class BrokerageMockError(Exception):
    """Base exception class. Caught by tools/_common.handle_errors."""

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class AccountNotFoundError(BrokerageMockError):
    code = "ACCOUNT_NOT_FOUND"


class SymbolNotFoundError(BrokerageMockError):
    code = "SYMBOL_NOT_FOUND"


class InsufficientCashError(BrokerageMockError):
    code = "INSUFFICIENT_CASH"


class InsufficientSharesError(BrokerageMockError):
    code = "INSUFFICIENT_SHARES"


class OrderNotFoundError(BrokerageMockError):
    code = "ORDER_NOT_FOUND"


class OrderNotPendingError(BrokerageMockError):
    code = "ORDER_NOT_PENDING"


class BadSideError(BrokerageMockError):
    code = "BAD_SIDE"


class BadOrderTypeError(BrokerageMockError):
    code = "BAD_ORDER_TYPE"


class FundNotFoundError(BrokerageMockError):
    code = "FUND_NOT_FOUND"


class InvalidAmountError(BrokerageMockError):
    code = "INVALID_AMOUNT"


class BadArgError(BrokerageMockError):
    code = "BAD_ARG"
