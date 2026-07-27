import json
import re
import sqlite3
from typing import Optional

from ..backends.db import next_counter
from ..utils.dates import current_date_iso
from ..utils.exceptions import (
    BadArgError,
    ReservationNotFoundError,
)
from ..utils.ids import now_iso_z, ticket_id as make_ticket_id
from .reservation_service import _classify_special_request


TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


class GuestService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ------------------------------------------------------------------
    # request_late_checkout
    # ------------------------------------------------------------------
    def request_late_checkout(self, reservation_id: str, new_time: str) -> dict:
        if not TIME_RE.match(new_time or ""):
            raise BadArgError("new_time must be HH:MM")
        row = self.conn.execute(
            "SELECT * FROM reservations WHERE reservation_id = ?",
            (reservation_id,),
        ).fetchone()
        if not row:
            raise ReservationNotFoundError("reservation not found")

        approved = False
        fee = 0
        reason: Optional[str] = None
        minute_value = int(new_time[:2]) * 60 + int(new_time[3:])

        if minute_value <= 12 * 60:
            approved = True
            fee = 0
        elif minute_value <= 14 * 60:
            approved = True
            fee = 2000
        elif minute_value <= 16 * 60:
            fee = 5000
            occupancy = self._next_night_occupancy(row["hotel_id"], row["check_out"])
            approved = occupancy < 0.85
            if not approved:
                fee = 0
                reason = "hotel is at capacity"
        else:
            approved = False
            fee = 0
            reason = "beyond latest late checkout time"

        sr_json = json.loads(row["special_requests_json"]) if row["special_requests_json"] else {}
        mods = sr_json.get("modifications", [])
        mods.append({
            "at": now_iso_z(),
            "field": "late_checkout",
            "requested": new_time,
            "approved": approved,
            "fee": fee,
            "reason": reason,
        })
        sr_json["modifications"] = mods
        if approved:
            sr_json["late_checkout_time"] = new_time

        self.conn.execute(
            "UPDATE reservations SET special_requests_json = ?, updated_at = ? WHERE reservation_id = ?",
            (json.dumps(sr_json, ensure_ascii=False), now_iso_z(), reservation_id),
        )

        return {
            "reservation_id": reservation_id,
            "approved": approved,
            "fee": fee,
            "new_time": new_time,
            "reason": reason,
        }

    def _next_night_occupancy(self, hotel_id: str, check_out_date: str) -> float:
        rows = self.conn.execute(
            """
            SELECT inventory_remaining, inventory_capacity FROM rate_plans
            WHERE hotel_id = ? AND date = ?
            """,
            (hotel_id, check_out_date),
        ).fetchall()
        if not rows:
            return 0.0
        ratios = []
        for r in rows:
            cap = max(int(r["inventory_capacity"]), 1)
            ratios.append(int(r["inventory_remaining"]) / cap)
        avg_remaining = sum(ratios) / len(ratios)
        return 1.0 - avg_remaining

    # ------------------------------------------------------------------
    # submit_special_request
    # ------------------------------------------------------------------
    def submit_special_request(self, reservation_id: str, text: str) -> dict:
        row = self.conn.execute(
            "SELECT reservation_id FROM reservations WHERE reservation_id = ?",
            (reservation_id,),
        ).fetchone()
        if not row:
            raise ReservationNotFoundError("reservation not found")
        if not text or not str(text).strip():
            raise BadArgError("text is required")

        seq = next_counter(self.conn, "ticket_seq")
        tkt = make_ticket_id(seq)
        status = _classify_special_request(text)
        now = now_iso_z()
        self.conn.execute(
            "INSERT INTO special_requests (ticket_id, reservation_id, text, status, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (tkt, reservation_id, text, status, now, now),
        )
        return {"ticket_id": tkt, "reservation_id": reservation_id, "status": status}

    # ------------------------------------------------------------------
    # get_user_bookings_summary
    # ------------------------------------------------------------------
    def get_user_bookings_summary(self, user_id: str) -> dict:
        res_rows = self.conn.execute(
            "SELECT * FROM reservations WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        if not res_rows:
            return {
                "user_id": user_id,
                "total_reservations": 0,
                "active_reservations": 0,
                "cancelled_reservations": 0,
                "total_spent_jpy": 0,
                "total_refunded_jpy": 0,
                "total_nights": 0,
                "cities": [],
                "upcoming_check_in": None,
                "loyalty_points_estimate": 0,
                "open_special_requests": 0,
            }

        total = len(res_rows)
        active = sum(1 for r in res_rows if r["status"] in ("confirmed", "modified"))
        cancelled = sum(1 for r in res_rows if r["status"] == "cancelled")

        total_spent = sum(int(r["total_charged"]) for r in res_rows if r["status"] in ("confirmed", "modified", "walked", "checked_out"))
        total_refunded = 0
        for r in res_rows:
            if r["status"] != "cancelled":
                continue
            # Prefer the persisted refund_amount from cancel_reservation
            # (see SPEC §3.8 penalty model). Fall back to total_charged
            # only if the cancellation record is missing (legacy rows).
            sr_json = json.loads(r["special_requests_json"]) if r["special_requests_json"] else {}
            cancellation = sr_json.get("cancellation") or {}
            if "refund_amount" in cancellation:
                total_refunded += int(cancellation["refund_amount"])
            else:
                total_refunded += int(r["total_charged"])
        current_date = current_date_iso(self.conn)

        total_nights = 0
        cities = set()
        upcoming: Optional[str] = None
        for r in res_rows:
            night_count = self.conn.execute(
                "SELECT COUNT(*) AS c FROM reservation_nights WHERE reservation_id = ?",
                (r["reservation_id"],),
            ).fetchone()["c"]
            if r["status"] in ("confirmed", "modified", "walked", "checked_out"):
                total_nights += int(night_count)
            hotel = self.conn.execute(
                "SELECT city FROM hotels WHERE hotel_id = ?", (r["hotel_id"],)
            ).fetchone()
            if hotel:
                cities.add(hotel["city"])
            if r["status"] in ("confirmed", "modified") and r["check_in"] >= current_date:
                if upcoming is None or r["check_in"] < upcoming:
                    upcoming = r["check_in"]

        open_req_count = self.conn.execute(
            """
            SELECT COUNT(*) AS c FROM special_requests sr
            JOIN reservations r ON r.reservation_id = sr.reservation_id
            WHERE r.user_id = ? AND sr.status IN ('open', 'pending_hotel', 'acknowledged')
            """,
            (user_id,),
        ).fetchone()["c"]

        return {
            "user_id": user_id,
            "total_reservations": total,
            "active_reservations": active,
            "cancelled_reservations": cancelled,
            "total_spent_jpy": int(total_spent),
            "total_refunded_jpy": int(total_refunded),
            "total_nights": int(total_nights),
            "cities": sorted(cities),
            "upcoming_check_in": upcoming,
            "loyalty_points_estimate": int(total_spent) // 100,
            "open_special_requests": int(open_req_count),
        }
