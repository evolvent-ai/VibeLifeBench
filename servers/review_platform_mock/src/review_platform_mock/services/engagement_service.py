"""Merchant Q&A + saved (收藏) merchants."""
import logging
import sqlite3
from typing import List

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import BadArgError
from ..utils.ids import qa_id as make_qa_id
from ._common import fetch_merchant, merchant_summary

logger = logging.getLogger(__name__)


class EngagementService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- Q&A -------------------------------------------------------------
    def get_merchant_qa(self, merchant_id: str) -> List[dict]:
        fetch_merchant(self.conn, merchant_id)  # raises MERCHANT_NOT_FOUND
        rows = self.conn.execute(
            """
            SELECT qa_id, merchant_id, user_id, question, answer, answered_by, created_at
            FROM merchant_qa WHERE merchant_id = ?
            ORDER BY created_at DESC, qa_id DESC
            """,
            (merchant_id,),
        ).fetchall()
        return [
            {
                "qa_id": r["qa_id"],
                "merchant_id": r["merchant_id"],
                "user_id": r["user_id"],
                "question": r["question"],
                "answer": r["answer"],
                "answered_by": r["answered_by"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]

    def ask_question(self, user_id: str, merchant_id: str, body: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        if not body:
            raise BadArgError("body is required")
        fetch_merchant(self.conn, merchant_id)  # raises MERCHANT_NOT_FOUND

        created_at = now_iso_z()
        seq = next_counter(self.conn, "qa_seq")
        qid = make_qa_id(seq)
        self.conn.execute(
            """
            INSERT INTO merchant_qa (qa_id, merchant_id, user_id, question, answer, answered_by, created_at)
            VALUES (?, ?, ?, ?, NULL, NULL, ?)
            """,
            (qid, merchant_id, user_id, body, created_at),
        )
        return {
            "qa_id": qid,
            "merchant_id": merchant_id,
            "user_id": user_id,
            "question": body,
            "answer": None,
            "answered_by": None,
            "created_at": created_at,
        }

    # ---- saved merchants -------------------------------------------------
    def save_merchant(self, user_id: str, merchant_id: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        fetch_merchant(self.conn, merchant_id)  # raises MERCHANT_NOT_FOUND
        saved_at = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO saved_merchants (user_id, merchant_id, saved_at)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, merchant_id) DO NOTHING
            """,
            (user_id, merchant_id, saved_at),
        )
        row = self.conn.execute(
            "SELECT saved_at FROM saved_merchants WHERE user_id = ? AND merchant_id = ?",
            (user_id, merchant_id),
        ).fetchone()
        return {
            "user_id": user_id,
            "merchant_id": merchant_id,
            "saved": True,
            "saved_at": row["saved_at"],
        }

    def list_saved_merchants(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            """
            SELECT m.*, s.saved_at AS saved_at
            FROM saved_merchants s JOIN merchants m ON m.merchant_id = s.merchant_id
            WHERE s.user_id = ? ORDER BY s.saved_at DESC, m.merchant_id ASC
            """,
            (user_id,),
        ).fetchall()
        out = []
        for r in rows:
            view = merchant_summary(r)
            view["saved_at"] = r["saved_at"]
            out.append(view)
        return out
