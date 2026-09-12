import sqlite3
from typing import Optional

from ..backends.db import next_counter
from ..utils.dates import now_iso_z, today_utc
from ..utils.exceptions import (
    CardNotFoundError,
    InvalidAmountError,
    OverpaymentError,
)
from ..utils.ids import payment_id, line_id


class PaymentService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def make_payment(self, card_id: str, amount_minor: int, source_hint: str) -> dict:
        if not isinstance(amount_minor, int) or amount_minor <= 0:
            raise InvalidAmountError("amount_minor must be a positive integer")

        card = self.conn.execute(
            "SELECT * FROM cards WHERE card_id = ?", (card_id,)
        ).fetchone()
        if not card:
            raise CardNotFoundError(f"card not found: {card_id}")

        statement_balance = int(card["statement_balance_minor"])
        unbilled_balance = int(card["unbilled_balance_minor"])
        total_outstanding = statement_balance + unbilled_balance

        if amount_minor > total_outstanding:
            raise OverpaymentError(
                f"amount {amount_minor} exceeds total outstanding {total_outstanding}"
            )

        # Apply to statement first
        applied_to_statement = min(amount_minor, statement_balance)
        remaining = amount_minor - applied_to_statement
        applied_to_unbilled = min(remaining, unbilled_balance)

        new_statement_balance = statement_balance - applied_to_statement
        new_unbilled_balance = unbilled_balance - applied_to_unbilled

        current_date = today_utc()
        seq = next_counter(self.conn, "payment_seq")
        pid = payment_id(current_date, seq)
        posted_at = now_iso_z()

        self.conn.execute("BEGIN IMMEDIATE;")
        try:
            self.conn.execute(
                """
                INSERT INTO payments (payment_id, card_id, posted_at, amount_minor,
                                      source_hint, applied_to_statement_minor,
                                      applied_to_unbilled_minor)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (pid, card_id, posted_at, amount_minor, source_hint or "",
                 applied_to_statement, applied_to_unbilled),
            )

            # Reduce balances and release available credit
            new_available = int(card["available_credit_minor"]) + amount_minor
            credit_limit = int(card["credit_limit_minor"])
            if new_available > credit_limit:
                new_available = credit_limit
            self.conn.execute(
                """
                UPDATE cards
                SET statement_balance_minor = ?,
                    unbilled_balance_minor = ?,
                    available_credit_minor = ?
                WHERE card_id = ?
                """,
                (new_statement_balance, new_unbilled_balance, new_available, card_id),
            )

            # Recompute min_payment_due against the new statement balance
            if new_statement_balance <= 0:
                self.conn.execute(
                    "UPDATE cards SET min_payment_due_minor = 0 WHERE card_id = ?",
                    (card_id,),
                )

            # If there's an open statement, mark payment line + maybe paid/partial
            if applied_to_statement > 0:
                self._apply_to_open_statement(card_id, applied_to_statement,
                                              source_hint, posted_at)

            self.conn.execute("COMMIT;")
        except Exception:
            self.conn.execute("ROLLBACK;")
            raise

        return {
            "payment_id": pid,
            "applied_to_statement_minor": applied_to_statement,
            "applied_to_unbilled_minor": applied_to_unbilled,
            "new_outstanding_minor": new_statement_balance + new_unbilled_balance,
        }

    def _apply_to_open_statement(
        self,
        card_id: str,
        amount: int,
        source_hint: str,
        posted_at: str,
    ) -> None:
        stmt = self.conn.execute(
            """
            SELECT * FROM statements
            WHERE card_id = ? AND status IN ('open','partial','overdue')
            ORDER BY period_end DESC LIMIT 1
            """,
            (card_id,),
        ).fetchone()
        if not stmt:
            return

        new_payments_minor = int(stmt["payments_minor"]) + amount
        new_closing = int(stmt["closing_balance_minor"]) - amount
        if new_closing < 0:
            new_closing = 0

        if new_closing == 0:
            new_status = "paid"
        elif new_payments_minor > 0:
            new_status = "partial"
        else:
            new_status = stmt["status"]

        self.conn.execute(
            """
            UPDATE statements
            SET payments_minor = ?, closing_balance_minor = ?, status = ?
            WHERE statement_id = ?
            """,
            (new_payments_minor, new_closing, new_status, stmt["statement_id"]),
        )

        seq = next_counter(self.conn, "line_seq")
        lid = line_id(seq)
        self.conn.execute(
            """
            INSERT INTO statement_lines (line_id, statement_id, posted_at, amount_minor,
                                         merchant_name, mcc, category, kind)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'payment')
            """,
            (lid, stmt["statement_id"], posted_at, -int(amount),
             f"Payment ({source_hint or 'unspecified'})", None, "payment"),
        )
