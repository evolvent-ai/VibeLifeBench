"""Reviews: list + write (recomputes merchant aggregate rating)."""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import BadArgError, BadRatingError
from ..utils.ids import review_id as make_review_id
from ._common import fetch_merchant

logger = logging.getLogger(__name__)


class ReviewService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_reviews(self, merchant_id: str, limit: int = 20) -> List[dict]:
        fetch_merchant(self.conn, merchant_id)  # raises MERCHANT_NOT_FOUND
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 200:
            limit = 200
        rows = self.conn.execute(
            """
            SELECT review_id, merchant_id, user_id, rating, body, image_captions, created_at
            FROM reviews WHERE merchant_id = ?
            ORDER BY created_at DESC, review_id DESC LIMIT ?
            """,
            (merchant_id, int(limit)),
        ).fetchall()
        return [self._view(r) for r in rows]

    def write_review(
        self,
        user_id: str,
        merchant_id: str,
        rating: int,
        body: str,
        image_captions: Optional[List[str]] = None,
    ) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        if rating is None or int(rating) < 1 or int(rating) > 5:
            raise BadRatingError("rating must be an integer 1-5")
        if not body:
            raise BadArgError("body is required")
        fetch_merchant(self.conn, merchant_id)  # raises MERCHANT_NOT_FOUND

        captions = ",".join(image_captions) if image_captions else None
        created_at = now_iso_z()

        self.conn.execute("SAVEPOINT write_review;")
        try:
            seq = next_counter(self.conn, "review_seq")
            rid = make_review_id(seq)
            self.conn.execute(
                """
                INSERT INTO reviews (
                    review_id, merchant_id, user_id, rating, body, image_captions, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (rid, merchant_id, user_id, int(rating), body, captions, created_at),
            )
            # Recompute the merchant's aggregate rating (stored as INTEGER tenths).
            agg = self.conn.execute(
                "SELECT COUNT(*) AS n, AVG(rating) AS avg_r FROM reviews WHERE merchant_id = ?",
                (merchant_id,),
            ).fetchone()
            n = int(agg["n"])
            avg_tenths = int(round(float(agg["avg_r"]) * 10)) if n else 0
            self.conn.execute(
                "UPDATE merchants SET rating_tenths = ?, review_count = ? WHERE merchant_id = ?",
                (avg_tenths, n, merchant_id),
            )
            self.conn.execute("RELEASE SAVEPOINT write_review;")
        except Exception:
            self.conn.execute("ROLLBACK TO SAVEPOINT write_review;")
            self.conn.execute("RELEASE SAVEPOINT write_review;")
            raise

        return {
            "review_id": rid,
            "merchant_id": merchant_id,
            "user_id": user_id,
            "rating": int(rating),
            "created_at": created_at,
            "merchant_new_rating": round(avg_tenths / 10.0, 1),
            "merchant_review_count": n,
        }

    @staticmethod
    def _view(r: sqlite3.Row) -> dict:
        captions = r["image_captions"]
        return {
            "review_id": r["review_id"],
            "merchant_id": r["merchant_id"],
            "user_id": r["user_id"],
            "rating": int(r["rating"]),
            "body": r["body"],
            "image_captions": [c for c in str(captions).split(",") if c] if captions else [],
            "created_at": r["created_at"],
        }
