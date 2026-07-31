"""Search + offer-synthesis service.

Deterministic — same query produces the same offers and the same offer_id
sequence (the counter table backs the IDs).
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional

from ..backends.sqlite_backend import SQLiteBackend
from ..utils import ids, timewin
from ..utils.exceptions import FlightBookingError

logger = logging.getLogger(__name__)

OFFER_TTL_MIN = 20
CARRIER_FARE_BASIS = {"ECONOMY": "YLX", "PREMIUM_ECONOMY": "WLX",
                      "BUSINESS": "JLX", "FIRST": "FLX"}


def _wall_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class SearchService:
    def __init__(self, backend: SQLiteBackend) -> None:
        self.backend = backend

    # ---------- public ----------
    def search_flights(self, *, origin: str, destination: str,
                       departure_date: str, return_date: Optional[str] = None,
                       adults: int = 1, children: int = 0, infants: int = 0,
                       cabin: str = "ECONOMY", currency: str = "CNY",
                       max_results: int = 20, sort: str = "price_asc",
                       non_stop: bool = False,
                       carriers: Optional[list[str]] = None) -> dict[str, Any]:
        now_iso = _wall_now_iso()
        outbound = self._candidate_itineraries(origin, destination, departure_date,
                                               cabin, carriers)
        inbound: list[dict[str, Any]] = []
        if return_date:
            inbound = self._candidate_itineraries(destination, origin, return_date,
                                              cabin, carriers)
            if not inbound:
                return self._empty_result()

        paid_pax = adults + children  # infants share revenue seat-less
        offers: list[dict[str, Any]] = []
        search_seed = ids.stable_hash_int(
            origin, destination, departure_date, return_date or "", cabin, adults
        )
        search_id = ids.search_id_gen(self.backend.conn, str(search_seed))

        if return_date:
            for o in outbound:
                for r in inbound:
                    offer = self._build_offer(o, r, cabin=cabin,
                                              paid_pax=paid_pax,
                                              currency=currency,
                                              now_dt_iso=now_iso,
                                              search_id=search_id)
                    offers.append(offer)
        else:
            for o in outbound:
                offer = self._build_offer(o, None, cabin=cabin,
                                          paid_pax=paid_pax,
                                          currency=currency,
                                          now_dt_iso=now_iso,
                                          search_id=search_id)
                offers.append(offer)

        # Optional non_stop filter removes synthesized connecting itineraries.
        if non_stop:
            offers = [o for o in offers
                      if all(s["stops"] == 0 for s in o["itinerary"]["slices"])]

        offers.sort(key=_sort_key(sort))
        total = len(offers)
        offers = offers[:max_results]
        for off in offers:
            self.backend.upsert_offer(off["offer_id"], off["_created_at"],
                                      off["_expires_at"], off["_payload"])
        # Strip internal fields before returning.
        cleaned = [_strip_internal(o) for o in offers]
        return {
            "offers": cleaned,
            "total": total,
            "returned": len(cleaned),
            "search_id": search_id,
        }

    def get_flight_offer(self, offer_id: str) -> dict[str, Any]:
        row = self.backend.get_offer(offer_id)
        if not row:
            raise FlightBookingError("offer_not_found", f"Unknown offer_id {offer_id}")
        payload = json.loads(row["payload_json"])
        segments = payload["segments"]
        return {
            "offer_id": offer_id,
            "total_price": payload["total_price"],
            "fare_breakdown": payload["fare_breakdown"],
            "segments": segments,
            "validating_carrier": payload["validating_carrier"],
            "ticketing_deadline": payload["ticketing_deadline"],
            "expires_at": row["expires_at"],
        }

    def get_seat_map(self, offer_id: Optional[str], pnr: Optional[str],
                     segment_idx: int) -> dict[str, Any]:
        if not offer_id and not pnr:
            raise FlightBookingError("offer_not_found",
                                     "Either offer_id or pnr is required")
        segment: dict[str, Any]
        if offer_id:
            off = self.backend.get_offer(offer_id)
            if not off:
                raise FlightBookingError("offer_not_found", f"{offer_id}")
            payload = json.loads(off["payload_json"])
            if segment_idx >= len(payload["segments"]):
                raise FlightBookingError("offer_not_found",
                                         f"segment {segment_idx} out of range")
            segment = payload["segments"][segment_idx]
        else:
            booking = self.backend.get_booking(pnr)  # type: ignore[arg-type]
            if not booking:
                raise FlightBookingError("booking_not_found", f"{pnr}")
            segs = json.loads(booking["segments_json"])
            if segment_idx >= len(segs):
                raise FlightBookingError("booking_not_found",
                                         f"segment {segment_idx} out of range")
            segment = segs[segment_idx]

        flight_no = segment["flight_no"]
        cabin = segment.get("cabin") or "ECONOMY"
        date = timewin.dt_date(segment["depart_dt"])
        # Live equipment from `flights` row.
        live_flight = self.backend.get_flight(flight_no, date)
        equipment = (live_flight["equipment"] if live_flight
                     else segment.get("equipment") or "738")

        layout = _generate_seat_map(flight_no, equipment, cabin)
        taken = self._collect_taken_seats(flight_no, date)
        for blk in layout:
            for row in blk["rows"]:
                for seat in row["seats"]:
                    if seat["seat"] in taken:
                        seat["available"] = False
        return {
            "flight_no": flight_no,
            "equipment": equipment,
            "cabin_layout": layout,
        }

    # ---------- internals ----------
    def _candidate_itineraries(
        self,
        origin: str,
        dest: str,
        date: str,
        cabin: str,
        carriers: Optional[list[str]],
    ) -> list[dict[str, Any]]:
        """Return direct and one-stop public-search itineraries.

        Task seeds frequently model real connections as separate flight rows.
        The original mock searched only exact origin/destination rows, making
        those seeded transit choices impossible to inspect or book through the
        public tools.  This keeps direct behavior and adds deterministic
        one-stop paths with a 45-minute to 24-hour connection window.
        """

        def leg_from_row(row: Any) -> dict[str, Any] | None:
            if carriers and row["carrier"] not in carriers:
                return None
            depart_date = str(row["depart_dt"])[:10]
            bucket = self.backend.get_fare_bucket(row["flight_no"], depart_date, cabin)
            if not bucket or bucket["seats_remaining"] <= 0:
                return None
            return {
                "flight_no": row["flight_no"], "origin": row["origin"],
                "dest": row["dest"], "depart_dt": row["depart_dt"],
                "arrive_dt": row["arrive_dt"], "equipment": row["equipment"],
                "base_price": row["base_price"], "carrier": row["carrier"],
                "price": bucket["price"], "seats_remaining": bucket["seats_remaining"],
                "date": depart_date,
            }

        direct_rows = self.backend.list_flights_for_route_date(origin, dest, date)
        itineraries: list[dict[str, Any]] = []
        for row in direct_rows:
            leg = leg_from_row(row)
            if leg:
                itineraries.append(self._path_from_legs([leg]))

        first_rows = self.backend.query_all(
            "SELECT * FROM flights WHERE origin=? AND substr(depart_dt,1,10)=? ORDER BY depart_dt, flight_no",
            (origin, date),
        )
        for first_row in first_rows:
            if first_row["dest"] == dest:
                continue
            first = leg_from_row(first_row)
            if first is None:
                continue
            second_rows = self.backend.query_all(
                "SELECT * FROM flights WHERE origin=? AND dest=? ORDER BY depart_dt, flight_no",
                (first["dest"], dest),
            )
            first_arrival = datetime.fromisoformat(str(first["arrive_dt"]).replace("Z", "+00:00"))
            for second_row in second_rows:
                second = leg_from_row(second_row)
                if second is None:
                    continue
                second_departure = datetime.fromisoformat(str(second["depart_dt"]).replace("Z", "+00:00"))
                connection_minutes = int((second_departure - first_arrival).total_seconds() // 60)
                if 45 <= connection_minutes <= 24 * 60:
                    itineraries.append(self._path_from_legs([first, second]))

        itineraries.sort(key=lambda path: (path["depart_dt"], path["arrive_dt"], tuple(
            leg["flight_no"] for leg in path["legs"]
        )))
        return itineraries

    @staticmethod
    def _path_from_legs(legs: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "origin": legs[0]["origin"],
            "dest": legs[-1]["dest"],
            "depart_dt": legs[0]["depart_dt"],
            "arrive_dt": legs[-1]["arrive_dt"],
            "carrier": legs[0]["carrier"],
            "price": sum(float(leg["price"]) for leg in legs),
            "seats_remaining": min(int(leg["seats_remaining"]) for leg in legs),
            "legs": legs,
        }

    def _build_offer(self, outbound: dict[str, Any], inbound: Optional[dict[str, Any]],
                     *, cabin: str, paid_pax: int, currency: str,
                     now_dt_iso: str, search_id: str) -> dict[str, Any]:
        paths = [outbound] + ([inbound] if inbound else [])
        legs = [leg for path in paths for leg in path["legs"]]
        per_leg_total = sum(float(leg["price"]) for leg in legs)
        total = round(per_leg_total * max(1, paid_pax), 2)
        # Fare breakdown: 78% base / 18% taxes / 4% fees, arbitrary mock split.
        base = round(total * 0.78, 2)
        taxes = round(total * 0.18, 2)
        fees = round(total - base - taxes, 2)

        segments: list[dict[str, Any]] = []
        for idx, leg in enumerate(legs):
            segments.append({
                "segment_idx": idx,
                "flight_no": leg["flight_no"],
                "origin": leg["origin"], "destination": leg["dest"],
                "depart_dt": leg["depart_dt"], "arrive_dt": leg["arrive_dt"],
                "equipment": leg["equipment"], "cabin": cabin,
                "fare_basis": CARRIER_FARE_BASIS.get(cabin, "YLX"),
                "baggage_allowance": _baggage_for(cabin),
                "fare_rules": _fare_rules_for(cabin),
            })

        slices: list[dict[str, Any]] = []
        segment_offset = 0
        for path in paths:
            path_legs = path["legs"]
            duration = timewin.duration_minutes(path["depart_dt"], path["arrive_dt"])
            slices.append({
                "origin": path["origin"], "destination": path["dest"],
                "depart_dt": path["depart_dt"], "arrive_dt": path["arrive_dt"],
                "duration_min": duration, "stops": max(0, len(path_legs) - 1),
                "segments": [{
                    "flight_no": leg["flight_no"], "cabin": cabin,
                    "depart_dt": leg["depart_dt"], "arrive_dt": leg["arrive_dt"],
                } for leg in path_legs],
            })
            segment_offset += len(path_legs)

        offer_id = ids.offer_id_gen(self.backend.conn, search_id)
        created = now_dt_iso
        expires = timewin.add_minutes(created, OFFER_TTL_MIN)
        ticketing_deadline = timewin.add_minutes(created, 60)
        seats_remaining_hint = min(int(leg["seats_remaining"]) for leg in legs)
        validating = legs[0]["carrier"]
        payload = {
            "total_price": {"amount": total, "currency": currency},
            "fare_breakdown": {
                "base": base, "taxes": taxes, "fees": fees, "currency": currency,
            },
            "segments": segments,
            "validating_carrier": validating,
            "ticketing_deadline": ticketing_deadline,
            "paid_pax": paid_pax,
            "cabin": cabin,
            "currency": currency,
        }
        return {
            "offer_id": offer_id,
            "total_price": {"amount": total, "currency": currency},
            "validating_carrier": validating,
            "itinerary": {"slices": slices},
            "seats_remaining_hint": seats_remaining_hint,
            "expires_at": expires,
            "_created_at": created,
            "_expires_at": expires,
            "_payload": payload,
        }

    def _collect_taken_seats(self, flight_no: str, date: str) -> set[str]:
        rows = self.backend.query_all(
            "SELECT sa.seat FROM seat_assignments sa "
            "JOIN bookings b ON b.pnr = sa.pnr "
            "WHERE b.status IN ('TICKETED','HOLD','CHANGED') "
            "AND EXISTS (SELECT 1 FROM json_each(b.segments_json) j "
            "WHERE CAST(json_extract(j.value,'$.segment_idx') AS INT) = sa.segment_idx "
            "AND json_extract(j.value,'$.flight_no') = ? "
            "AND substr(json_extract(j.value,'$.depart_dt'),1,10) = ?)",
            (flight_no, date),
        )
        return {r["seat"] for r in rows}

    def _empty_result(self) -> dict[str, Any]:
        return {"offers": [], "total": 0, "returned": 0,
                "search_id": ids.search_id_gen(self.backend.conn, "empty")}


# -------- helpers (module-private) --------
def _sort_key(sort: str):
    def price_key(o: dict[str, Any]) -> Any:
        return o["total_price"]["amount"]

    def duration_key(o: dict[str, Any]) -> Any:
        return sum(s["duration_min"] for s in o["itinerary"]["slices"])

    def depart_key(o: dict[str, Any]) -> Any:
        return o["itinerary"]["slices"][0]["depart_dt"]

    return {"price_asc": price_key,
            "duration_asc": duration_key,
            "depart_asc": depart_key}.get(sort, price_key)


def _strip_internal(o: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in o.items() if not k.startswith("_")}


def _baggage_for(cabin: str) -> dict[str, int]:
    return {
        "ECONOMY": {"checked_kg": 23, "carry_on_kg": 7},
        "PREMIUM_ECONOMY": {"checked_kg": 32, "carry_on_kg": 10},
        "BUSINESS": {"checked_kg": 46, "carry_on_kg": 14},
        "FIRST": {"checked_kg": 46, "carry_on_kg": 14},
    }.get(cabin, {"checked_kg": 23, "carry_on_kg": 7})


def _fare_rules_for(cabin: str) -> dict[str, Any]:
    if cabin == "ECONOMY":
        return {"refundable": False, "changeable": True, "change_fee": 450}
    if cabin == "PREMIUM_ECONOMY":
        return {"refundable": False, "changeable": True, "change_fee": 300}
    # BUSINESS / FIRST
    return {"refundable": True, "changeable": True, "change_fee": 0}


# Equipment → (rows, letters).
_EQUIPMENT_LAYOUT = {
    "788": (32, "ABCDEGHJK"),    # 3-3-3
    "789": (38, "ABCDEGHJK"),
    "77W": (44, "ABCDEFGHJK"),   # 3-4-3
    "738": (28, "ABCDEF"),       # 3-3
    "333": (40, "ABCDEGHJK"),    # 2-4-2 approximated as 3-3-3
}


def valid_seats_for_equipment(equipment: str) -> set[str]:
    """Return the set of seat labels the given aircraft layout supports."""
    rows, letters = _EQUIPMENT_LAYOUT.get(equipment, (28, "ABCDEF"))
    return {f"{r}{letter}" for r in range(1, rows + 1) for letter in letters}


def _generate_seat_map(flight_no: str, equipment: str, cabin: str) -> list[dict[str, Any]]:
    rows, letters = _EQUIPMENT_LAYOUT.get(equipment, (28, "ABCDEF"))

    # Cabin ranges — small slice for first, medium for premium, rest economy.
    business_rows = (1, 4) if equipment in ("788", "789", "77W", "333") else (1, 2)
    premium_rows = (business_rows[1] + 1, business_rows[1] + 4)
    economy_rows = (premium_rows[1] + 1, rows)

    def build(cab_name: str, r0: int, r1: int) -> dict[str, Any]:
        out_rows = []
        for r in range(r0, r1 + 1):
            seats = []
            for letter in letters:
                characteristics = []
                if letter in {"A", letters[-1]}:
                    characteristics.append("WINDOW")
                if letter in {"C", "D"} and cab_name != "BUSINESS":
                    characteristics.append("AISLE")
                if r in {12, 13}:  # mock exit rows
                    characteristics.append("EXIT")
                    characteristics.append("EXTRA_LEGROOM")
                price_delta = 0
                if cab_name == "BUSINESS":
                    price_delta = 0
                elif cab_name == "PREMIUM_ECONOMY":
                    price_delta = 120
                elif "EXTRA_LEGROOM" in characteristics:
                    price_delta = 180
                elif "WINDOW" in characteristics or "AISLE" in characteristics:
                    price_delta = 40
                seats.append({
                    "seat": f"{r}{letter}",
                    "available": True,
                    "characteristics": characteristics,
                    "price_delta": {"amount": price_delta, "currency": "CNY"},
                })
            out_rows.append({"row_number": r, "seats": seats})
        return {"cabin": cab_name, "rows": out_rows}

    blocks: list[dict[str, Any]] = []
    blocks.append(build("BUSINESS", business_rows[0], business_rows[1]))
    blocks.append(build("PREMIUM_ECONOMY", premium_rows[0], premium_rows[1]))
    blocks.append(build("ECONOMY", economy_rows[0], economy_rows[1]))
    return blocks
