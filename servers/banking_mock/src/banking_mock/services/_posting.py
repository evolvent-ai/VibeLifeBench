"""Low-level account posting helpers shared across services.

These functions operate on an existing ``sqlite3.Connection``. They do NOT
manage transactions on their own — callers wrap multi-step posts (e.g.
transfers) in ``SAVEPOINT``s when atomicity is required.
"""
import sqlite3
from typing import Optional

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import (
    AccountFrozenError,
    AccountNotFoundError,
    InsufficientFundsError,
)
from ..utils.ids import tx_id as make_tx_id


def fetch_account(conn: sqlite3.Connection, account_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM accounts WHERE account_id = ?", (account_id,)
    ).fetchone()
    if not row:
        raise AccountNotFoundError(f"account not found: {account_id}")
    return row


def post_transaction(
    conn: sqlite3.Connection,
    *,
    account_id: str,
    amount_minor: int,
    kind: str,
    sim_date: str,
    posted_at: Optional[str] = None,
    counterparty: Optional[str] = None,
    memo: Optional[str] = None,
    allow_frozen: bool = False,
) -> dict:
    """Apply ``amount_minor`` (signed) to an account and insert a tx row.

    Positive ``amount_minor`` is an inflow; negative is an outflow.
    Raises ``AccountFrozenError`` / ``InsufficientFundsError`` if the
    debit cannot be applied (overridable by ``allow_frozen=True`` for
    interest accrual on frozen savings, etc.).
    """
    acct = fetch_account(conn, account_id)
    if amount_minor < 0 and not allow_frozen and int(acct["frozen"]) == 1:
        raise AccountFrozenError(f"account {account_id} is frozen")

    current_balance = int(acct["balance_minor"])
    new_balance = current_balance + int(amount_minor)
    if amount_minor < 0 and new_balance < 0:
        raise InsufficientFundsError(
            f"insufficient funds in {account_id}: balance {current_balance}, "
            f"requested {abs(amount_minor)}"
        )

    seq = next_counter(conn, "tx_seq")
    tx_identifier = make_tx_id(seq, sim_date)
    ts = posted_at or now_iso_z()

    conn.execute(
        """
        UPDATE accounts SET balance_minor = ? WHERE account_id = ?
        """,
        (new_balance, account_id),
    )
    conn.execute(
        """
        INSERT INTO transactions (
            tx_id, account_id, posted_at, amount_minor, kind,
            counterparty, memo, balance_after_minor
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            tx_identifier,
            account_id,
            ts,
            int(amount_minor),
            kind,
            counterparty,
            memo,
            new_balance,
        ),
    )
    return {
        "tx_id": tx_identifier,
        "posted_at": ts,
        "balance_after_minor": new_balance,
    }
