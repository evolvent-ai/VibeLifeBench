"""团购套餐 (deals) + 订座/预约 (reservations)."""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import now_iso_z, parse_datetime
from ..utils.exceptions import (
    BadArgError,
    DealUnavailableError,
    PartySizeError,
    ReservationNotFoundError,
)
from ..utils.ids import reservation_id as make_reservation_id
from ._common import deal_view, fetch_deal, fetch_merchant

logger = logging.getLogger(__name__)


class BookingService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- deals -----------------------------------------------------------
    def list_merchant_deals(self, merchant_id: str) -> List[dict]:
        fetch_merchant(self.conn, merchant_id)  # raises MERCHANT_NOT_FOUND
        rows = self.conn.execute(
            "SELECT * FROM deals WHERE merchant_id = ? ORDER BY deal_id ASC",
            (merchant_id,),
        ).fetchall()
        return [deal_view(r) for r in rows]

    def get_deal(self, deal_id: str) -> dict:
        return deal_view(fetch_deal(self.conn, deal_id))

    # ---- reservations ----------------------------------------------------
    def reserve(
        self,
        user_id: str,
        merchant_id: str,
        datetime: str,
        party_size: int,
        deal_id: Optional[str] = None,
    ) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        if party_size is None or int(party_size) < 1:
            raise BadArgError("party_size must be a positive integer")
        when = parse_datetime(datetime)  # raises BAD_DATE
        merchant = fetch_merchant(self.conn, merchant_id)  # raises MERCHANT_NOT_FOUND

        max_party = int(merchant["max_party_size"])
        if max_party and int(party_size) > max_party:
            raise PartySizeError(
                f"party_size {party_size} exceeds merchant max {max_party}"
            )

        if deal_id is not None:
            deal = fetch_deal(self.conn, deal_id)  # raises DEAL_NOT_FOUND
            if deal["merchant_id"] != merchant_id:
                raise BadArgError("deal_id does not belong to this merchant")
            if deal["status"] != "active":
                raise DealUnavailableError(
                    f"deal {deal_id} is not active (status={deal['status']})"
                )

        created_at = now_iso_z()
        normalized = when.strftime("%Y-%m-%dT%H:%M:%S")

        self.conn.execute("SAVEPOINT reserve;")
        try:
            seq = next_counter(self.conn, "reservation_seq")
            rid = make_reservation_id(seq)
            self.conn.execute(
                """
                INSERT INTO reservations (
                    reservation_id, user_id, merchant_id, datetime,
                    party_size, deal_id, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'confirmed', ?)
                """,
                (rid, user_id, merchant_id, normalized, int(party_size), deal_id, created_at),
            )
            self.conn.execute("RELEASE SAVEPOINT reserve;")
        except Exception:
            self.conn.execute("ROLLBACK TO SAVEPOINT reserve;")
            self.conn.execute("RELEASE SAVEPOINT reserve;")
            raise

        return {
            "reservation_id": rid,
            "user_id": user_id,
            "merchant_id": merchant_id,
            "merchant_name": merchant["name"],
            "datetime": normalized,
            "party_size": int(party_size),
            "deal_id": deal_id,
            "status": "confirmed",
            "created_at": created_at,
        }

    def list_reservations(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            """
            SELECT r.*, m.name AS merchant_name
            FROM reservations r JOIN merchants m ON m.merchant_id = r.merchant_id
            WHERE r.user_id = ? ORDER BY r.datetime DESC, r.reservation_id DESC
            """,
            (user_id,),
        ).fetchall()
        return [self._view(r) for r in rows]

    def cancel_reservation(self, reservation_id: str) -> dict:
        row = self.conn.execute(
            "SELECT * FROM reservations WHERE reservation_id = ?", (reservation_id,)
        ).fetchone()
        if not row:
            raise ReservationNotFoundError(f"reservation not found: {reservation_id}")
        if row["status"] != "cancelled":
            self.conn.execute(
                "UPDATE reservations SET status = 'cancelled' WHERE reservation_id = ?",
                (reservation_id,),
            )
        return {"reservation_id": reservation_id, "status": "cancelled"}

    @staticmethod
    def _view(r: sqlite3.Row) -> dict:
        return {
            "reservation_id": r["reservation_id"],
            "user_id": r["user_id"],
            "merchant_id": r["merchant_id"],
            "merchant_name": r["merchant_name"],
            "datetime": r["datetime"],
            "party_size": int(r["party_size"]),
            "deal_id": r["deal_id"],
            "status": r["status"],
            "created_at": r["created_at"],
        }
