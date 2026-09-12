import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import add_days, now_iso_z, today_utc
from ..utils.exceptions import (
    DisputeAlreadyOpenError,
    TransactionNotFoundError,
    CardNotFoundError,
)
from ..utils.ids import dispute_id


class DisputeService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _resolve_tx(self, tx_id: str):
        """Return (card_id, posted_at, amount) for a tx_id from either
        unbilled_transactions or statement_lines.
        """
        row = self.conn.execute(
            """
            SELECT card_id, posted_at, amount_minor
            FROM unbilled_transactions WHERE tx_id = ?
            """,
            (tx_id,),
        ).fetchone()
        if row:
            return row["card_id"], row["posted_at"], int(row["amount_minor"])
        row = self.conn.execute(
            """
            SELECT s.card_id AS card_id, sl.posted_at AS posted_at,
                   sl.amount_minor AS amount_minor
            FROM statement_lines sl
            JOIN statements s ON s.statement_id = sl.statement_id
            WHERE sl.line_id = ?
            """,
            (tx_id,),
        ).fetchone()
        if row:
            return row["card_id"], row["posted_at"], int(row["amount_minor"])
        return None

    def dispute_transaction(self, tx_id: str, reason: str) -> dict:
        resolved = self._resolve_tx(tx_id)
        if not resolved:
            raise TransactionNotFoundError(f"transaction not found: {tx_id}")
        card_id, _posted_at, _amount = resolved

        existing = self.conn.execute(
            """
            SELECT dispute_id FROM disputes
            WHERE tx_id = ? AND status = 'under_review'
            """,
            (tx_id,),
        ).fetchone()
        if existing:
            raise DisputeAlreadyOpenError(
                f"dispute already under review for tx {tx_id}: {existing['dispute_id']}"
            )

        current_date = today_utc()
        seq = next_counter(self.conn, "dispute_seq")
        did = dispute_id(current_date, seq)
        expected_resolution = add_days(current_date, 30)
        opened_at = now_iso_z()

        self.conn.execute(
            """
            INSERT INTO disputes (dispute_id, card_id, tx_id, reason, status,
                                  opened_at, expected_resolution_date)
            VALUES (?, ?, ?, ?, 'under_review', ?, ?)
            """,
            (did, card_id, tx_id, reason or "", opened_at, expected_resolution),
        )

        return {
            "dispute_id": did,
            "status": "under_review",
            "expected_resolution_date": expected_resolution,
        }

    def list_disputes(self, card_id: str, status_filter: Optional[str] = None) -> List[dict]:
        row = self.conn.execute(
            "SELECT 1 FROM cards WHERE card_id = ?", (card_id,)
        ).fetchone()
        if not row:
            raise CardNotFoundError(f"card not found: {card_id}")

        params = [card_id]
        sql = "SELECT * FROM disputes WHERE card_id = ?"
        if status_filter:
            sql += " AND status = ?"
            params.append(status_filter)
        sql += " ORDER BY opened_at DESC"

        rows = self.conn.execute(sql, params).fetchall()
        return [
            {
                "dispute_id": r["dispute_id"],
                "card_id": r["card_id"],
                "tx_id": r["tx_id"],
                "reason": r["reason"],
                "status": r["status"],
                "opened_at": r["opened_at"],
                "expected_resolution_date": r["expected_resolution_date"],
                "resolved_at": r["resolved_at"],
            }
            for r in rows
        ]
