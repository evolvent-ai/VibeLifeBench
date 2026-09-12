import sqlite3
from typing import List, Optional

from ..utils.dates import now_iso_z
from ..utils.exceptions import CardNotFoundError


def _row_to_card_summary(r: sqlite3.Row) -> dict:
    return {
        "card_id": r["card_id"],
        "issuer": r["issuer"],
        "product_name": r["product_name"],
        "masked_no": r["masked_no"],
        "type": r["type"],
        "credit_limit_minor": int(r["credit_limit_minor"]),
        "available_credit_minor": int(r["available_credit_minor"]),
        "statement_balance_minor": int(r["statement_balance_minor"]),
        "min_payment_due_minor": int(r["min_payment_due_minor"]),
        "due_date": r["due_date"],
        "status": r["status"],
    }


class CardService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list_cards(self, user_id: str) -> List[dict]:
        rows = self.conn.execute(
            "SELECT * FROM cards WHERE user_id = ? ORDER BY card_id",
            (user_id,),
        ).fetchall()
        return [_row_to_card_summary(r) for r in rows]

    def _get_card_row(self, card_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM cards WHERE card_id = ?", (card_id,)
        ).fetchone()
        if not row:
            raise CardNotFoundError(f"card not found: {card_id}")
        return row

    def get_card(self, card_id: str) -> dict:
        row = self._get_card_row(card_id)
        # last 5 transactions = newest among unbilled + statement_lines
        unbilled = self.conn.execute(
            """
            SELECT tx_id AS id, posted_at, amount_minor, merchant_name, mcc, category, kind,
                   NULL AS statement_id
            FROM unbilled_transactions
            WHERE card_id = ?
            """,
            (card_id,),
        ).fetchall()
        billed = self.conn.execute(
            """
            SELECT sl.line_id AS id, sl.posted_at, sl.amount_minor, sl.merchant_name,
                   sl.mcc, sl.category, sl.kind, sl.statement_id
            FROM statement_lines sl
            JOIN statements s ON s.statement_id = sl.statement_id
            WHERE s.card_id = ?
            """,
            (card_id,),
        ).fetchall()

        combined = []
        for r in list(unbilled) + list(billed):
            combined.append({
                "id": r["id"],
                "posted_at": r["posted_at"],
                "amount_minor": int(r["amount_minor"]),
                "merchant_name": r["merchant_name"],
                "mcc": r["mcc"],
                "category": r["category"],
                "kind": r["kind"],
                "statement_id": r["statement_id"],
            })
        combined.sort(key=lambda x: x["posted_at"], reverse=True)
        recent = combined[:5]

        rewards = self.conn.execute(
            "SELECT points_balance FROM rewards_balances WHERE card_id = ?",
            (card_id,),
        ).fetchone()
        points_balance = int(rewards["points_balance"]) if rewards else 0

        return {
            "card_id": row["card_id"],
            "user_id": row["user_id"],
            "issuer": row["issuer"],
            "product_name": row["product_name"],
            "masked_no": row["masked_no"],
            "type": row["type"],
            "credit_limit_minor": int(row["credit_limit_minor"]),
            "available_credit_minor": int(row["available_credit_minor"]),
            "statement_balance_minor": int(row["statement_balance_minor"]),
            "unbilled_balance_minor": int(row["unbilled_balance_minor"]),
            "min_payment_due_minor": int(row["min_payment_due_minor"]),
            "due_date": row["due_date"],
            "status": row["status"],
            "cycle_start_day": int(row["cycle_start_day"]),
            "cycle_end_day": int(row["cycle_end_day"]),
            "grace_period_days": int(row["grace_period_days"]),
            "interest_apr_bp": int(row["interest_apr_bp"]),
            "points_balance": points_balance,
            "recent_transactions": recent,
        }

    def set_status(self, card_id: str, status: str) -> dict:
        self._get_card_row(card_id)
        if status not in ("active", "frozen", "expired", "closed"):
            raise ValueError(f"invalid status: {status}")
        self.conn.execute(
            "UPDATE cards SET status = ? WHERE card_id = ?",
            (status, card_id),
        )
        row = self._get_card_row(card_id)
        return _row_to_card_summary(row)

    def freeze(self, card_id: str) -> dict:
        return self.set_status(card_id, "frozen")

    def unfreeze(self, card_id: str) -> dict:
        return self.set_status(card_id, "active")
