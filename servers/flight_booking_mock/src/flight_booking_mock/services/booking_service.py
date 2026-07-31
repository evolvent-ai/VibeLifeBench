"""Booking lifecycle service: create/get/list/cancel/change/check_in."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional

from ..backends.sqlite_backend import SQLiteBackend
from ..utils import ids, timewin
from ..utils.exceptions import FlightBookingError
from .search_service import valid_seats_for_equipment


def _wall_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class BookingService:
    def __init__(self, backend: SQLiteBackend) -> None:
        self.backend = backend

    # ---------- create ----------
    def create_booking(self, *, offer_id: str, passengers: list[dict[str, Any]],
                       contact: dict[str, str], payment: dict[str, Any],
                       seat_selections: Optional[list[dict[str, Any]]] = None,
                       hold: bool = False) -> dict[str, Any]:
        offer_row = self.backend.get_offer(offer_id)
        if not offer_row:
            raise FlightBookingError("offer_not_found", offer_id)
        now_iso = _wall_now_iso()

        payload = json.loads(offer_row["payload_json"])
        priced_price = offer_row["priced_price"]
        if priced_price is None:
            # auto-price at creation; use current bucket totals
            priced_price = payload["total_price"]["amount"]

        if payment.get("card_last4") == "0000":
            raise FlightBookingError("payment_declined_mock",
                                     "card_last4=0000 is rigged to decline")

        segments = payload["segments"]
        cabin = payload.get("cabin") or "ECONOMY"
        pax_count = max(1, len(passengers))

        # Check seats available in each fare bucket
        for seg in segments:
            date = timewin.dt_date(seg["depart_dt"])
            bucket = self.backend.get_fare_bucket(seg["flight_no"], date, cabin)
            if not bucket or bucket["seats_remaining"] < pax_count:
                raise FlightBookingError(
                    "inventory_gone",
                    f"{seg['flight_no']} {cabin} on {date}: not enough seats",
                )

        # Validate seat selections.
        seat_selections = seat_selections or []
        seen_seats: set[tuple[int, str]] = set()
        for sel in seat_selections:
            seg_idx = int(sel["segment_idx"])
            if seg_idx >= len(segments):
                raise FlightBookingError("seat_unavailable",
                                         f"segment {seg_idx} out of range")
            seg = segments[seg_idx]
            date = timewin.dt_date(seg["depart_dt"])
            key = (seg_idx, sel["seat"])
            if key in seen_seats:
                raise FlightBookingError("seat_unavailable",
                                         f"duplicate seat {sel['seat']} on segment {seg_idx}")
            seen_seats.add(key)
            live = self.backend.get_flight(seg["flight_no"], date)
            live_eq = live["equipment"] if live else seg.get("equipment", "738")
            if sel["seat"] not in valid_seats_for_equipment(live_eq):
                raise FlightBookingError(
                    "seat_unavailable",
                    f"{sel['seat']} does not exist on {live_eq}",
                )
            if self.backend.seat_taken_on_segment(seg["flight_no"], date, sel["seat"]):
                raise FlightBookingError("seat_unavailable",
                                         f"{sel['seat']} already taken")

        # Reserve seats
        for seg in segments:
            date = timewin.dt_date(seg["depart_dt"])
            self.backend.decrement_fare_bucket_seats(
                seg["flight_no"], date, cabin, pax_count)

        # PNR derived deterministically from offer+contact+counter.
        pnr_seed = f"{offer_id}|{contact.get('email', '')}"
        pnr = ids.pnr_gen(self.backend.conn, pnr_seed)
        # Extremely unlikely collision, but if it ever happens, keep bumping.
        while self.backend.get_booking(pnr):
            pnr = ids.pnr_gen(self.backend.conn, pnr_seed)

        status = "HOLD" if hold else "TICKETED"
        created_at = now_iso
        user_id = contact.get("email")
        booking_segments = []
        for seg in segments:
            booking_segments.append({
                "segment_idx": seg["segment_idx"],
                "flight_no": seg["flight_no"],
                "origin": seg["origin"], "dest": seg["destination"],
                "depart_dt": seg["depart_dt"], "arrive_dt": seg["arrive_dt"],
                "cabin": seg["cabin"], "equipment": seg.get("equipment", ""),
            })

        history = [{"at": created_at, "event": "CREATED",
                    "detail": f"status={status} offer={offer_id}"}]

        self.backend.insert_booking({
            "pnr": pnr, "user_id": user_id, "offer_id": offer_id,
            "status": status,
            "paid_amount": priced_price,
            "currency": payload["total_price"]["currency"],
            "created_at": created_at,
            "segments": booking_segments,
            "passengers": passengers,
            "contact": contact,
            "history": history,
        })

        # Persist seat selections
        for sel in seat_selections:
            self.backend.insert_seat_assignment(
                pnr, int(sel["segment_idx"]),
                int(sel["pax_idx"]), sel["seat"])

        # Ticket numbers: one per pax per segment.
        ticket_numbers = []
        for p_idx in range(len(passengers)):
            for s_idx in range(len(segments)):
                ticket_numbers.append(
                    ids.ticket_number_gen(self.backend.conn, f"{pnr}|{p_idx}|{s_idx}")
                )

        segments_out = []
        for seg in booking_segments:
            seat = None
            for sel in seat_selections:
                if int(sel["segment_idx"]) == seg["segment_idx"] and int(sel.get("pax_idx", 0)) == 0:
                    seat = sel["seat"]
                    break
            segments_out.append({
                "segment_idx": seg["segment_idx"],
                "flight_no": seg["flight_no"],
                "cabin": seg["cabin"],
                "seat": seat,
            })

        return {
            "pnr": pnr,
            "status": status,
            "total_paid": {"amount": priced_price,
                           "currency": payload["total_price"]["currency"]},
            "ticket_numbers": ticket_numbers,
            "segments": segments_out,
            "created_at": created_at,
        }

    # ---------- get ----------
    def get_booking(self, pnr: str) -> dict[str, Any]:
        row = self.backend.get_booking(pnr)
        if not row:
            raise FlightBookingError("booking_not_found", pnr)
        segs = json.loads(row["segments_json"])
        pax = json.loads(row["passengers_json"])
        contact = json.loads(row["contact_json"])
        history = json.loads(row["history_json"])
        seat_rows = self.backend.get_seat_assignments(pnr)
        seats_by_seg: dict[int, list[dict[str, Any]]] = {}
        for sr in seat_rows:
            seats_by_seg.setdefault(sr["segment_idx"], []).append(
                {"pax_idx": sr["pax_idx"], "seat": sr["seat"]})

        segments_out = []
        for s in segs:
            # Look up live flight_status for the segment (best-effort).
            date = timewin.dt_date(s["depart_dt"])
            fs = self.backend.get_flight_status(s["flight_no"], date)
            seg_status = fs["status"] if fs else "SCHEDULED"
            segments_out.append({
                "segment_idx": s["segment_idx"],
                "flight_no": s["flight_no"],
                "origin": s["origin"], "destination": s.get("dest") or s.get("destination"),
                "depart_dt": s["depart_dt"], "arrive_dt": s["arrive_dt"],
                "cabin": s["cabin"], "status": seg_status,
                "seats": seats_by_seg.get(s["segment_idx"], []),
            })

        return {
            "pnr": row["pnr"], "status": row["status"],
            "total_paid": {"amount": row["paid_amount"], "currency": row["currency"]},
            "passengers": [{"given_name": p["given_name"],
                            "family_name": p["family_name"],
                            "type": p["type"]} for p in pax],
            "segments": segments_out,
            "contact": contact,
            "created_at": row["created_at"],
            "history": history,
        }

    # ---------- list ----------
    def list_bookings(self, *, user_id: Optional[str] = None,
                      email: Optional[str] = None,
                      status: Optional[str] = None,
                      page: int = 1, page_size: int = 20) -> dict[str, Any]:
        rows = self.backend.list_bookings(user_id=user_id, email=email, status=status)
        total = len(rows)
        page = max(1, page)
        page_size = max(1, min(50, page_size))
        start = (page - 1) * page_size
        window = rows[start:start + page_size]

        result = []
        for r in window:
            segs = json.loads(r["segments_json"])
            first_depart = segs[0]["depart_dt"] if segs else ""
            airports = [segs[0]["origin"]] if segs else []
            for s in segs:
                airports.append(s.get("dest") or s.get("destination"))
            route = "-".join(airports)
            result.append({
                "pnr": r["pnr"], "status": r["status"],
                "total_paid": {"amount": r["paid_amount"], "currency": r["currency"]},
                "first_depart_dt": first_depart,
                "route_summary": route,
            })
        total_pages = max(1, (total + page_size - 1) // page_size)
        return {
            "bookings": result, "total": total,
            "page": page, "total_pages": total_pages,
        }

    # ---------- cancel ----------
    def cancel_booking(self, *, pnr: str,
                       reason: Optional[str] = None) -> dict[str, Any]:
        row = self.backend.get_booking(pnr)
        if not row:
            raise FlightBookingError("booking_not_found", pnr)
        if row["status"] == "CANCELLED":
            raise FlightBookingError("already_cancelled", pnr)

        offer_row = self.backend.get_offer(row["offer_id"])
        refundable = True
        fees_withheld = 0.0
        method = "ORIGINAL_FORM"
        segs = json.loads(row["segments_json"])
        if offer_row:
            payload = json.loads(offer_row["payload_json"])
            seg_rules = payload["segments"][0].get("fare_rules", {})
            refundable = bool(seg_rules.get("refundable", False))
            if not refundable:
                # Charge a mock cancel fee = min(50% of paid, change_fee*2 if present)
                cf = seg_rules.get("change_fee") or 900
                fees_withheld = round(min(float(row["paid_amount"]) * 0.5,
                                          float(cf) * 2), 2)
                method = "VOUCHER"
        refund_amount = round(max(0.0, float(row["paid_amount"]) - fees_withheld), 2)

        # Restore seats
        pax_list = json.loads(row["passengers_json"])
        pax_count = max(1, len(pax_list))
        for s in segs:
            date = timewin.dt_date(s["depart_dt"])
            self.backend.increment_fare_bucket_seats(
                s["flight_no"], date, s["cabin"], pax_count)

        history = json.loads(row["history_json"])
        cancelled_at = _wall_now_iso()
        history.append({"at": cancelled_at, "event": "CANCELLED",
                        "detail": reason or ""})
        self.backend.update_booking(
            pnr, status="CANCELLED", history_json=json.dumps(history))

        return {
            "pnr": pnr, "status": "CANCELLED",
            "refund": {
                "refundable": refundable,
                "amount": {"amount": refund_amount, "currency": row["currency"]},
                "fees_withheld": {"amount": fees_withheld,
                                  "currency": row["currency"]},
                "method": method,
            },
            "cancelled_at": cancelled_at,
        }

    # ---------- change ----------
    def change_booking(self, *, pnr: str, new_offer_id: str,
                       segment_indices: Optional[list[int]] = None) -> dict[str, Any]:
        row = self.backend.get_booking(pnr)
        if not row:
            raise FlightBookingError("booking_not_found", pnr)
        offer_row = self.backend.get_offer(new_offer_id)
        if not offer_row:
            raise FlightBookingError("offer_not_found", new_offer_id)

        old_payload = None
        old_offer_row = self.backend.get_offer(row["offer_id"])
        if old_offer_row:
            old_payload = json.loads(old_offer_row["payload_json"])
            old_rules = old_payload["segments"][0].get("fare_rules", {})
            if not old_rules.get("changeable", False):
                raise FlightBookingError("non_changeable_fare", pnr)

        new_payload = json.loads(offer_row["payload_json"])
        new_segs = new_payload["segments"]
        old_segs = json.loads(row["segments_json"])

        target_idx = segment_indices if segment_indices is not None else list(
            range(len(old_segs)))

        cabin = old_segs[0]["cabin"] if old_segs else "ECONOMY"
        pax_count = max(1, len(json.loads(row["passengers_json"])))
        new_cabin = new_segs[0]["cabin"] if new_segs else cabin

        # Up-front inventory check for the new segments.
        new_segment_checks: list[tuple[str, str]] = []
        for ns in new_segs[:len(target_idx)]:
            date = timewin.dt_date(ns["depart_dt"])
            bucket = self.backend.get_fare_bucket(ns["flight_no"], date, new_cabin)
            if not bucket or bucket["seats_remaining"] < pax_count:
                raise FlightBookingError(
                    "inventory_gone",
                    f"{ns['flight_no']} {new_cabin} on {date}: not enough seats")
            new_segment_checks.append((ns["flight_no"], date))

        # Splice in new segments (truncate to match indices)
        replacement = []
        ni = 0
        for idx in range(len(old_segs)):
            if idx in target_idx and ni < len(new_segs):
                ns = new_segs[ni]
                ni += 1
                replacement.append({
                    "segment_idx": idx,
                    "flight_no": ns["flight_no"],
                    "origin": ns["origin"], "dest": ns["destination"],
                    "depart_dt": ns["depart_dt"], "arrive_dt": ns["arrive_dt"],
                    "cabin": ns["cabin"], "equipment": ns.get("equipment", ""),
                })
            else:
                replacement.append(old_segs[idx])

        old_price = float(row["paid_amount"])
        new_price = float(offer_row["priced_price"] or new_payload["total_price"]["amount"])
        fare_diff = round(new_price - old_price, 2)
        change_fee = float((old_payload or {}).get("segments", [{}])[0]
                           .get("fare_rules", {}).get("change_fee", 0) or 0) if old_payload else 0.0
        currency = row["currency"]

        history = json.loads(row["history_json"])
        changed_at = _wall_now_iso()
        history.append({"at": changed_at, "event": "CHANGED",
                        "detail": f"new_offer={new_offer_id} diff={fare_diff}"})

        with self.backend.transaction() as conn:
            for idx in target_idx:
                if idx < len(old_segs):
                    s = old_segs[idx]
                    date = timewin.dt_date(s["depart_dt"])
                    conn.execute(
                        "UPDATE fare_buckets SET seats_remaining = seats_remaining + ? "
                        "WHERE flight_no=? AND date=? AND cabin=?",
                        (pax_count, s["flight_no"], date, s["cabin"]),
                    )
                    conn.execute(
                        "DELETE FROM seat_assignments WHERE pnr=? AND segment_idx=?",
                        (pnr, idx),
                    )
            for flight_no, date in new_segment_checks:
                conn.execute(
                    "UPDATE fare_buckets SET seats_remaining = MAX(0, seats_remaining - ?) "
                    "WHERE flight_no=? AND date=? AND cabin=?",
                    (pax_count, flight_no, date, new_cabin),
                )
            conn.execute(
                "UPDATE bookings SET status=?, offer_id=?, paid_amount=?, "
                "segments_json=?, history_json=? WHERE pnr=?",
                (
                    "CHANGED", new_offer_id, new_price + change_fee,
                    json.dumps(replacement), json.dumps(history), pnr,
                ),
            )

        return {
            "pnr": pnr, "status": "CHANGED",
            "fare_difference": {"amount": fare_diff, "currency": currency},
            "change_fee": {"amount": change_fee, "currency": currency},
            "new_segments": [{
                "segment_idx": s["segment_idx"], "flight_no": s["flight_no"],
                "depart_dt": s["depart_dt"], "arrive_dt": s["arrive_dt"],
                "cabin": s["cabin"],
            } for s in replacement if s["segment_idx"] in target_idx],
            "changed_at": changed_at,
        }

    # ---------- check-in ----------
    def check_in(self, *, pnr: str, segment_idx: int,
                 pax_indices: Optional[list[int]] = None,
                 preferred_seats: Optional[list[dict[str, Any]]] = None) -> dict[str, Any]:
        row = self.backend.get_booking(pnr)
        if not row:
            raise FlightBookingError("booking_not_found", pnr)
        segs = json.loads(row["segments_json"])
        if segment_idx >= len(segs):
            raise FlightBookingError("booking_not_found",
                                     f"segment_idx {segment_idx} out of range")
        seg = segs[segment_idx]
        date = timewin.dt_date(seg["depart_dt"])
        fs = self.backend.get_flight_status(seg["flight_no"], date)
        if fs and fs["status"] == "CANCELLED":
            raise FlightBookingError("flight_cancelled",
                                     f"{seg['flight_no']} on {date}")

        now_iso = _wall_now_iso()
        pax_list = json.loads(row["passengers_json"])
        target = pax_indices if pax_indices is not None else list(range(len(pax_list)))
        pref_map: dict[int, str] = {}
        for p in (preferred_seats or []):
            pref_map[int(p["pax_idx"])] = p["seat"]

        # Existing seat assignments
        existing = {(r["pax_idx"]): dict(r) for r in self.backend.get_seat_assignments(pnr)
                    if r["segment_idx"] == segment_idx}

        # Live equipment drives the pool of acceptable auto-assigned seats.
        live = self.backend.get_flight(seg["flight_no"], date)
        live_eq = live["equipment"] if live else seg.get("equipment", "738")
        valid_seats = valid_seats_for_equipment(live_eq)
        out: list[dict[str, Any]] = []
        taken_now: set[str] = set()
        for px in target:
            if px in existing and existing[px].get("boarding_pass_id"):
                raise FlightBookingError(
                    "already_checked_in",
                    f"pax {px} on segment {segment_idx}")
            seat = pref_map.get(px) or (existing[px]["seat"] if px in existing else None)
            if seat is not None and seat not in valid_seats:
                seat = None
            if seat is None:
                seat = _pick_available_seat(
                    valid_seats,
                    lambda s: (
                        s in taken_now
                        or self.backend.seat_taken_on_segment(
                            seg["flight_no"], date, s)
                    ),
                )
            if self.backend.seat_taken_on_segment(seg["flight_no"], date, seat) and \
               existing.get(px, {}).get("seat") != seat:
                raise FlightBookingError("seat_unavailable", seat)
            taken_now.add(seat)
            bp = ids.boarding_pass_id_gen(self.backend.conn, f"{pnr}|{segment_idx}|{px}")
            self.backend.mark_checked_in(pnr, segment_idx, px, seat, bp)
            out.append({"pax_idx": px, "seat": seat, "boarding_pass_id": bp})

        boarding_time = timewin.add_minutes(seg["depart_dt"], -40)
        gate = fs["gate"] if fs else None
        terminal = fs["terminal"] if fs else None

        history = json.loads(row["history_json"])
        history.append({"at": now_iso, "event": "CHECKED_IN",
                        "detail": f"segment={segment_idx} pax={target}"})
        self.backend.update_booking(pnr, history_json=json.dumps(history))

        return {
            "pnr": pnr,
            "segment_idx": segment_idx,
            "checked_in": out,
            "boarding_time": boarding_time,
            "gate": gate,
            "terminal": terminal,
        }


def _pick_available_seat(valid_seats: set[str], is_taken: Any) -> str:
    """Pick a deterministic available seat from the live layout."""
    if not valid_seats:
        raise FlightBookingError("seat_unavailable", "no seats in layout")
    ordered = sorted(valid_seats, key=lambda s: (int("".join(c for c in s if c.isdigit())), s))
    for seat in ordered:
        if not is_taken(seat):
            return seat
    raise FlightBookingError("seat_unavailable", "all seats taken")
