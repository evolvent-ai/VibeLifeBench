import json
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import current_date_iso, iter_nights
from ..utils.exceptions import (
    AlreadyCancelledError,
    BadArgError,
    BadDateRangeError,
    HotelNotFoundError,
    ModifyNoAvailabilityError,
    RatePlanNotFoundError,
    ReservationNotFoundError,
    SoldOutError,
    UncancellableError,
)
from ..utils.ids import confirmation_code, now_iso_z, reservation_id as make_res_id
from .availability_service import make_rate_plan_id, parse_rate_plan_id, resolve_room_type


logger = logging.getLogger(__name__)


class ReservationService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _fetch_reservation_row(self, reservation_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM reservations WHERE reservation_id = ?",
            (reservation_id,),
        ).fetchone()
        if not row:
            raise ReservationNotFoundError("reservation not found")
        return row

    def _hotel_row(self, hotel_id: str) -> sqlite3.Row:
        row = self.conn.execute("SELECT * FROM hotels WHERE hotel_id = ?", (hotel_id,)).fetchone()
        if not row:
            raise HotelNotFoundError("hotel not found")
        return row

    def _get_plan_rows(
        self,
        hotel_id: str,
        room_type: str,
        flavor: str,
        nights: List[str],
    ) -> List[sqlite3.Row]:
        rows = self.conn.execute(
            """
            SELECT * FROM rate_plans
            WHERE hotel_id = ? AND room_type = ? AND flavor = ? AND date IN (%s)
            ORDER BY date
            """ % (",".join(["?"] * len(nights))),
            [hotel_id, room_type, flavor, *nights],
        ).fetchall()
        return rows

    def _reservation_to_dict(self, row: sqlite3.Row, include_details: bool = True) -> dict:
        hotel_row = self.conn.execute(
            "SELECT name FROM hotels WHERE hotel_id = ?", (row["hotel_id"],)
        ).fetchone()
        hotel_name = hotel_row["name"] if hotel_row else row["hotel_id"]
        guest_profile = json.loads(row["guest_profile_json"])
        guest_name = (
            f"{guest_profile.get('first_name', '')} {guest_profile.get('last_name', '')}".strip()
            or "Guest"
        )
        out = {
            "reservation_id": row["reservation_id"],
            "confirmation_code": row["confirmation_code"],
            "status": row["status"],
            "total_charged": int(row["total_charged"]),
            "currency": row["currency"],
            "hotel_id": row["hotel_id"],
            "hotel_name": hotel_name,
            "check_in": row["check_in"],
            "check_out": row["check_out"],
            "room_type": row["room_type"],
            "guest_name": guest_name,
            "refundable": bool(row["refundable"]),
            "refundable_until": row["refundable_until"],
        }
        if include_details:
            night_rows = self.conn.execute(
                "SELECT date, nightly_price, rate_plan_row_id FROM reservation_nights "
                "WHERE reservation_id = ? ORDER BY date",
                (row["reservation_id"],),
            ).fetchall()
            sreq_rows = self.conn.execute(
                "SELECT ticket_id, text, status FROM special_requests "
                "WHERE reservation_id = ? ORDER BY created_at",
                (row["reservation_id"],),
            ).fetchall()
            sr_json = json.loads(row["special_requests_json"]) if row["special_requests_json"] else {}
            out["nights"] = [
                {
                    "date": n["date"],
                    "nightly_price": int(n["nightly_price"]),
                    "rate_plan_row_id": int(n["rate_plan_row_id"]),
                }
                for n in night_rows
            ]
            out["special_requests"] = [
                {
                    "ticket_id": s["ticket_id"],
                    "text": s["text"],
                    "status": s["status"],
                }
                for s in sreq_rows
            ]
            out["created_at"] = row["created_at"]
            out["modifications"] = sr_json.get("modifications", [])
            if "late_checkout_time" in sr_json:
                out["late_checkout_time"] = sr_json["late_checkout_time"]
            if "walked_from" in sr_json:
                out["walked_from"] = sr_json["walked_from"]
            if "walk_info" in sr_json:
                out["walk_info"] = sr_json["walk_info"]
            if "compensation" in sr_json:
                out["compensation"] = sr_json["compensation"]
        return out

    def _push_notification(self, channel: str, payload: dict) -> None:
        self.conn.execute(
            "INSERT INTO notifications (created_at, channel, payload_json) VALUES (?, ?, ?)",
            (now_iso_z(), channel, json.dumps(payload, ensure_ascii=False)),
        )

    # ------------------------------------------------------------------
    # create_reservation
    # ------------------------------------------------------------------
    def create_reservation(
        self,
        rate_plan_id: str,
        guest_profile: dict,
        payment_method_id: str,
        special_requests: Optional[str] = None,
    ) -> dict:
        if not payment_method_id or not isinstance(payment_method_id, str):
            raise BadArgError("payment_method_id must be a non-empty string")
        if not isinstance(guest_profile, dict):
            raise BadArgError("guest_profile must be an object")
        for field in ("first_name", "last_name", "email", "phone", "user_id"):
            if not guest_profile.get(field):
                raise BadArgError(f"guest_profile.{field} is required")

        try:
            hotel_id, slug, flavor, check_in, check_out = parse_rate_plan_id(rate_plan_id)
        except ValueError as e:
            raise RatePlanNotFoundError(f"invalid rate_plan_id: {e}")

        room_type = resolve_room_type(self.conn, hotel_id, slug)
        if not room_type:
            raise RatePlanNotFoundError("rate plan not found (no matching room type)")

        nights = iter_nights(check_in, check_out)
        plan_rows = self._get_plan_rows(hotel_id, room_type, flavor, nights)
        if len(plan_rows) != len(nights):
            raise RatePlanNotFoundError("rate plan not found for all nights")
        if any(int(r["inventory_remaining"]) <= 0 for r in plan_rows):
            raise SoldOutError("no inventory")
        currencies = {str(r["currency"]) for r in plan_rows}
        if len(currencies) != 1:
            raise RatePlanNotFoundError("rate plan spans multiple currencies")
        currency = next(iter(currencies))

        current_date = current_date_iso(self.conn)

        total_charged = sum(int(r["nightly_price"]) for r in plan_rows)
        # refundable_until logic: earliest non-null across nights
        refundable_untils = [r["refundable_until"] for r in plan_rows if r["refundable_until"]]
        reservation_refundable = False
        reservation_refundable_until = None
        if refundable_untils and len(refundable_untils) == len(plan_rows):
            reservation_refundable_until = min(refundable_untils)
            if reservation_refundable_until[:10] >= current_date:
                reservation_refundable = True

        seq = next_counter(self.conn, "reservation_seq")
        reservation_id_str = make_res_id(current_date, seq)
        code = confirmation_code(reservation_id_str)
        created_at = now_iso_z()

        self.conn.execute(
            """
            INSERT INTO reservations (
              reservation_id, confirmation_code, user_id, hotel_id,
              check_in, check_out, room_type, flavor, status,
              total_charged, currency, refundable, refundable_until,
              created_at, updated_at, guest_profile_json, payment_method_id, special_requests_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'confirmed', ?, ?, ?, ?, ?, ?, ?, ?, '{}')
            """,
            (
                reservation_id_str,
                code,
                guest_profile["user_id"],
                hotel_id,
                check_in,
                check_out,
                room_type,
                flavor,
                total_charged,
                currency,
                1 if reservation_refundable else 0,
                reservation_refundable_until,
                created_at,
                created_at,
                json.dumps(guest_profile, ensure_ascii=False),
                payment_method_id,
            ),
        )

        # Insert nights + decrement inventory
        for r in plan_rows:
            self.conn.execute(
                "INSERT INTO reservation_nights (reservation_id, date, rate_plan_row_id, nightly_price) VALUES (?, ?, ?, ?)",
                (reservation_id_str, r["date"], int(r["rate_plan_row_id"]), int(r["nightly_price"])),
            )
            self.conn.execute(
                "UPDATE rate_plans SET inventory_remaining = inventory_remaining - 1 WHERE rate_plan_row_id = ?",
                (int(r["rate_plan_row_id"]),),
            )

        if special_requests:
            self._insert_special_request(reservation_id_str, special_requests)

        hotel_row = self.conn.execute(
            "SELECT name FROM hotels WHERE hotel_id = ?", (hotel_id,)
        ).fetchone()

        self._push_notification(
            "email",
            {
                "kind": "confirmation",
                "reservation_id": reservation_id_str,
                "confirmation_code": code,
                "hotel_id": hotel_id,
                "check_in": check_in,
                "check_out": check_out,
                "total_charged": total_charged,
                "currency": currency,
            },
        )

        guest_name = f"{guest_profile['first_name']} {guest_profile['last_name']}"
        return {
            "reservation_id": reservation_id_str,
            "confirmation_code": code,
            "status": "confirmed",
            "total_charged": total_charged,
            "currency": currency,
            "hotel_id": hotel_id,
            "hotel_name": hotel_row["name"] if hotel_row else hotel_id,
            "check_in": check_in,
            "check_out": check_out,
            "room_type": room_type,
            "guest_name": guest_name,
            "refundable": reservation_refundable,
            "refundable_until": reservation_refundable_until,
        }

    def _insert_special_request(self, reservation_id_str: str, text: str) -> dict:
        seq = next_counter(self.conn, "ticket_seq")
        from ..utils.ids import ticket_id as make_ticket_id
        tkt = make_ticket_id(seq)
        status = _classify_special_request(text)
        now = now_iso_z()
        self.conn.execute(
            "INSERT INTO special_requests (ticket_id, reservation_id, text, status, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (tkt, reservation_id_str, text, status, now, now),
        )
        return {"ticket_id": tkt, "reservation_id": reservation_id_str, "status": status}

    # ------------------------------------------------------------------
    # get / list
    # ------------------------------------------------------------------
    def get_reservation(self, reservation_id: str) -> dict:
        row = self._fetch_reservation_row(reservation_id)
        return self._reservation_to_dict(row, include_details=True)

    def list_reservations(self, user_id: str) -> dict:
        rows = self.conn.execute(
            "SELECT reservation_id FROM reservations WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
        ids = [r["reservation_id"] for r in rows]
        return {"user_id": user_id, "count": len(ids), "reservation_ids": ids}

    # ------------------------------------------------------------------
    # modify_reservation
    # ------------------------------------------------------------------
    def modify_reservation(
        self,
        reservation_id: str,
        new_check_in: Optional[str] = None,
        new_check_out: Optional[str] = None,
        new_room_type: Optional[str] = None,
    ) -> dict:
        if new_check_in is None and new_check_out is None and new_room_type is None:
            raise BadArgError("must provide at least one of new_check_in, new_check_out, new_room_type")
        row = self._fetch_reservation_row(reservation_id)
        if row["status"] in ("cancelled", "walked", "checked_out"):
            raise ModifyNoAvailabilityError(f"cannot modify reservation in status '{row['status']}'")

        hotel_id = row["hotel_id"]
        flavor = row["flavor"]
        orig_check_in = row["check_in"]
        orig_check_out = row["check_out"]
        orig_room_type = row["room_type"]

        target_check_in = new_check_in or orig_check_in
        target_check_out = new_check_out or orig_check_out
        target_room_type = new_room_type or orig_room_type

        try:
            new_nights = iter_nights(target_check_in, target_check_out)
        except ValueError:
            raise BadDateRangeError("new_check_out must be after new_check_in")

        # current nights rows (for inventory release)
        orig_night_rows = self.conn.execute(
            "SELECT date, rate_plan_row_id FROM reservation_nights WHERE reservation_id = ?",
            (reservation_id,),
        ).fetchall()

        # Release old inventory in-memory (do not touch DB yet; we run in a savepoint)
        self.conn.execute("SAVEPOINT modify_res;")
        try:
            # increment old inventory
            for n in orig_night_rows:
                self.conn.execute(
                    "UPDATE rate_plans SET inventory_remaining = inventory_remaining + 1 WHERE rate_plan_row_id = ?",
                    (int(n["rate_plan_row_id"]),),
                )
            # Look up new rate plans
            plan_rows = self._get_plan_rows(hotel_id, target_room_type, flavor, new_nights)
            if len(plan_rows) != len(new_nights) or any(int(r["inventory_remaining"]) <= 0 for r in plan_rows):
                self.conn.execute("ROLLBACK TO SAVEPOINT modify_res;")
                self.conn.execute("RELEASE SAVEPOINT modify_res;")
                raise ModifyNoAvailabilityError("no availability for new dates/room")

            # Compute fee
            current_date = current_date_iso(self.conn)
            fee = 0
            date_shift = (target_check_in != orig_check_in) or (target_check_out != orig_check_out)
            refundable_until = row["refundable_until"]
            if date_shift and refundable_until and refundable_until[:10] < current_date:
                fee = 3000
            elif date_shift and not refundable_until:
                fee = 3000

            # remove old night rows
            self.conn.execute(
                "DELETE FROM reservation_nights WHERE reservation_id = ?",
                (reservation_id,),
            )
            new_total = 0
            for r in plan_rows:
                new_total += int(r["nightly_price"])
                self.conn.execute(
                    "INSERT INTO reservation_nights (reservation_id, date, rate_plan_row_id, nightly_price) VALUES (?, ?, ?, ?)",
                    (reservation_id, r["date"], int(r["rate_plan_row_id"]), int(r["nightly_price"])),
                )
                self.conn.execute(
                    "UPDATE rate_plans SET inventory_remaining = inventory_remaining - 1 WHERE rate_plan_row_id = ?",
                    (int(r["rate_plan_row_id"]),),
                )

            price_delta = new_total - int(row["total_charged"])
            # SPEC §3.7: `fees` are penalty-only and returned separately.
            # `total_charged` tracks nightly total, never includes the fee.
            new_total_charged = new_total

            # refundable_until recompute from new plan rows
            new_refundable_untils = [r["refundable_until"] for r in plan_rows if r["refundable_until"]]
            new_refundable = False
            new_ru = None
            if new_refundable_untils and len(new_refundable_untils) == len(plan_rows):
                new_ru = min(new_refundable_untils)
                if new_ru[:10] >= current_date:
                    new_refundable = True

            sr_json = json.loads(row["special_requests_json"]) if row["special_requests_json"] else {}
            mods = sr_json.get("modifications", [])
            change_entry = {"at": now_iso_z(), "fee": fee}
            if new_check_in:
                change_entry["field"] = "check_in"
                change_entry["from"] = orig_check_in
                change_entry["to"] = target_check_in
                mods.append(dict(change_entry))
            if new_check_out:
                change_entry = {"at": now_iso_z(), "fee": fee, "field": "check_out", "from": orig_check_out, "to": target_check_out}
                mods.append(change_entry)
            if new_room_type:
                change_entry = {"at": now_iso_z(), "fee": fee, "field": "room_type", "from": orig_room_type, "to": target_room_type}
                mods.append(change_entry)
            sr_json["modifications"] = mods

            self.conn.execute(
                """
                UPDATE reservations
                SET status = 'modified', check_in = ?, check_out = ?, room_type = ?,
                    total_charged = ?, refundable = ?, refundable_until = ?,
                    updated_at = ?, special_requests_json = ?
                WHERE reservation_id = ?
                """,
                (
                    target_check_in,
                    target_check_out,
                    target_room_type,
                    new_total_charged,
                    1 if new_refundable else 0,
                    new_ru,
                    now_iso_z(),
                    json.dumps(sr_json, ensure_ascii=False),
                    reservation_id,
                ),
            )

            self.conn.execute("RELEASE SAVEPOINT modify_res;")
        except ModifyNoAvailabilityError:
            raise
        except Exception as e:
            self.conn.execute("ROLLBACK TO SAVEPOINT modify_res;")
            self.conn.execute("RELEASE SAVEPOINT modify_res;")
            raise

        updated_row = self._fetch_reservation_row(reservation_id)
        return {
            "reservation_id": reservation_id,
            "fees": fee,
            "price_delta": price_delta,
            "updated_reservation": self._reservation_to_dict(updated_row, include_details=True),
        }

    # ------------------------------------------------------------------
    # cancel_reservation
    # ------------------------------------------------------------------
    def cancel_reservation(self, reservation_id: str) -> dict:
        row = self._fetch_reservation_row(reservation_id)
        if row["status"] == "cancelled":
            raise AlreadyCancelledError("already cancelled")
        if row["status"] in ("checked_out", "walked"):
            raise UncancellableError("cannot cancel in current status")

        current_date = current_date_iso(self.conn)
        total_charged = int(row["total_charged"])
        flavor = row["flavor"]
        refundable_until = row["refundable_until"]
        is_refundable_now = bool(row["refundable"]) and (refundable_until is None or refundable_until[:10] >= current_date)

        # Compute refund / penalty
        if is_refundable_now:
            refund_amount = total_charged
            penalty = 0
        elif flavor == "prepaid":
            refund_amount = 0
            penalty = total_charged
        else:
            # flex/semi past window: penalty = 1 night
            night_rows = self.conn.execute(
                "SELECT nightly_price FROM reservation_nights WHERE reservation_id = ? ORDER BY date LIMIT 1",
                (reservation_id,),
            ).fetchall()
            one_night_price = int(night_rows[0]["nightly_price"]) if night_rows else 0
            penalty = one_night_price
            refund_amount = total_charged - penalty

        # Release inventory
        night_rows = self.conn.execute(
            "SELECT rate_plan_row_id FROM reservation_nights WHERE reservation_id = ?",
            (reservation_id,),
        ).fetchall()
        for n in night_rows:
            self.conn.execute(
                "UPDATE rate_plans SET inventory_remaining = inventory_remaining + 1 WHERE rate_plan_row_id = ?",
                (int(n["rate_plan_row_id"]),),
            )

        # SPEC §3.8: persist refund/penalty so downstream summaries
        # (get_user_bookings_summary.total_refunded_jpy) can read the
        # authoritative refunded amount instead of recomputing from
        # total_charged.
        currency = str(row["currency"])
        sr_json = json.loads(row["special_requests_json"]) if row["special_requests_json"] else {}
        sr_json["cancellation"] = {
            "at": now_iso_z(),
            "refund_amount": int(refund_amount),
            "penalty": int(penalty),
            "currency": currency,
            "was_refundable": bool(is_refundable_now),
        }
        self.conn.execute(
            "UPDATE reservations SET status = 'cancelled', updated_at = ?, special_requests_json = ? WHERE reservation_id = ?",
            (now_iso_z(), json.dumps(sr_json, ensure_ascii=False), reservation_id),
        )

        self._push_notification(
            "email",
            {
                "kind": "cancellation",
                "reservation_id": reservation_id,
                "refund_amount": refund_amount,
                "penalty": penalty,
                "currency": currency,
            },
        )

        return {
            "reservation_id": reservation_id,
            "status": "cancelled",
            "refund_amount": refund_amount,
            "penalty": penalty,
            "currency": currency,
        }


def _classify_special_request(text: str) -> str:
    lower = (text or "").lower()
    if any(k in lower for k in ("crib", "cot", "baby")):
        return "pending_hotel"
    if any(k in lower for k in ("allergy", "allergic")):
        return "pending_hotel"
    if "early check-in" in lower:
        return "pending_hotel"
    if any(k in lower for k in ("high floor", "quiet room", "extra pillow", "view")):
        return "acknowledged"
    return "open"
