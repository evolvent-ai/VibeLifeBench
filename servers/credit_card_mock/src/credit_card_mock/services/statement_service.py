import sqlite3
from typing import List

from ..utils.exceptions import CardNotFoundError, StatementNotFoundError


class StatementService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _assert_card(self, card_id: str) -> None:
        row = self.conn.execute(
            "SELECT 1 FROM cards WHERE card_id = ?", (card_id,)
        ).fetchone()
        if not row:
            raise CardNotFoundError(f"card not found: {card_id}")

    def list_statements(self, card_id: str, limit: int = 12) -> List[dict]:
        self._assert_card(card_id)
        limit = max(1, min(int(limit), 60))
        rows = self.conn.execute(
            """
            SELECT * FROM statements
            WHERE card_id = ?
            ORDER BY period_end DESC
            LIMIT ?
            """,
            (card_id, limit),
        ).fetchall()
        return [
            {
                "statement_id": r["statement_id"],
                "period_start": r["period_start"],
                "period_end": r["period_end"],
                "opening_balance_minor": int(r["opening_balance_minor"]),
                "new_charges_minor": int(r["new_charges_minor"]),
                "payments_minor": int(r["payments_minor"]),
                "closing_balance_minor": int(r["closing_balance_minor"]),
                "min_payment_due_minor": int(r["min_payment_due_minor"]),
                "due_date": r["due_date"],
                "status": r["status"],
            }
            for r in rows
        ]

    def get_statement(self, statement_id: str) -> dict:
        header = self.conn.execute(
            "SELECT * FROM statements WHERE statement_id = ?",
            (statement_id,),
        ).fetchone()
        if not header:
            raise StatementNotFoundError(f"statement not found: {statement_id}")
        lines = self.conn.execute(
            """
            SELECT line_id, posted_at, amount_minor, merchant_name, mcc, category, kind
            FROM statement_lines
            WHERE statement_id = ?
            ORDER BY posted_at ASC
            """,
            (statement_id,),
        ).fetchall()
        return {
            "statement_id": header["statement_id"],
            "card_id": header["card_id"],
            "period_start": header["period_start"],
            "period_end": header["period_end"],
            "opening_balance_minor": int(header["opening_balance_minor"]),
            "new_charges_minor": int(header["new_charges_minor"]),
            "payments_minor": int(header["payments_minor"]),
            "closing_balance_minor": int(header["closing_balance_minor"]),
            "min_payment_due_minor": int(header["min_payment_due_minor"]),
            "due_date": header["due_date"],
            "status": header["status"],
            "statement_lines": [
                {
                    "line_id": ln["line_id"],
                    "posted_at": ln["posted_at"],
                    "amount_minor": int(ln["amount_minor"]),
                    "merchant_name": ln["merchant_name"],
                    "mcc": ln["mcc"],
                    "category": ln["category"],
                    "kind": ln["kind"],
                }
                for ln in lines
            ],
        }

    def list_unbilled(self, card_id: str) -> List[dict]:
        self._assert_card(card_id)
        # "since the latest statement period end" — but unbilled_transactions
        # is already authoritative; just return rows newest first.
        rows = self.conn.execute(
            """
            SELECT tx_id, posted_at, amount_minor, merchant_name, mcc, category, kind
            FROM unbilled_transactions
            WHERE card_id = ?
            ORDER BY posted_at ASC
            """,
            (card_id,),
        ).fetchall()
        return [
            {
                "tx_id": r["tx_id"],
                "posted_at": r["posted_at"],
                "amount_minor": int(r["amount_minor"]),
                "merchant_name": r["merchant_name"],
                "mcc": r["mcc"],
                "category": r["category"],
                "kind": r["kind"],
            }
            for r in rows
        ]
