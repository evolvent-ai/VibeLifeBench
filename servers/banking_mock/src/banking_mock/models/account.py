from dataclasses import dataclass
from typing import Optional


@dataclass
class Account:
    """A user-owned bank account.

    Money is stored as integer minor units (cents / 分).
    """
    account_id: str
    user_id: str
    type: str  # checking | savings | money_market | education_fund
    name: str
    balance_minor: int
    currency: str
    opened_at: str
    frozen: bool = False


@dataclass
class Transaction:
    """A posted transaction against an account.

    `amount_minor` is signed from the account's perspective: positive for
    inflows (deposit, transfer_in, interest), negative for outflows
    (withdrawal, transfer_out, payment, fee).
    """
    tx_id: str
    account_id: str
    posted_at: str
    amount_minor: int
    kind: str  # deposit | withdrawal | transfer_in | transfer_out | payment | fee | interest
    counterparty: Optional[str]
    memo: Optional[str]
    balance_after_minor: int
