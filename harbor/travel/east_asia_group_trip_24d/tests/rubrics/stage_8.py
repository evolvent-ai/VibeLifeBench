"""Stage 8: bind scoring to four real reservations, capacity, refundability, dates and durable IDs."""
from __future__ import annotations

from loguru import logger

from ._helpers import _hotel_reservation_details, _tool_calls, _tool_name_matches, _workspace_file_text


def _selected(env) -> tuple[list[dict], list[dict]]:
    active = [r for r in _hotel_reservation_details(env) if str(r.get("status") or "").casefold() in {"confirmed", "modified"}]
    tokyo = [r for r in active if r.get("hotel_id") == "htl_shinjuku_grand" and r.get("room_type") == "Superior Twin" and str(r.get("check_in"))[:10] == "2026-06-05" and str(r.get("check_out"))[:10] == "2026-06-08"]
    seoul = [r for r in active if r.get("hotel_id") == "htl_myeongdong_plaza" and r.get("room_type") == "Superior Twin" and str(r.get("check_in"))[:10] == "2026-06-08" and str(r.get("check_out"))[:10] == "2026-06-10"]
    return tokyo, seoul


def s8_exact_hotels_reserved(env) -> bool:
    tokyo, seoul = _selected(env)
    calls = _tool_calls(env, 8)
    creates = sum(_tool_name_matches(str(c.get("name") or ""), "hotel_booking", "create_reservation") for c in calls)
    # Each real room has max occupancy two; two Tokyo rooms cover four and two Seoul rooms cover three.
    state_ok = len(tokyo) == 2 and len(seoul) == 2 and all(bool(r.get("refundable")) and r.get("refundable_until") for r in tokyo + seoul)
    result = bool(state_ok and creates >= 4)
    logger.info("s8_exact_hotels_reserved: {}", "PASS" if result else "FAIL")
    return result


def s8_booking_register_matches_policies(env) -> bool:
    tokyo, seoul = _selected(env)
    reservations = tokyo + seoul
    if len(tokyo) != 2 or len(seoul) != 2:
        return False
    text = _workspace_file_text(env, "/workspace/bookings.md").casefold()
    for reservation in reservations:
        rid = str(reservation.get("reservation_id") or "").casefold()
        deadline = str(reservation.get("refundable_until") or "").casefold()
        amount = str(reservation.get("total_charged") or "")
        currency = str(reservation.get("currency") or "").casefold()
        if not all((rid, deadline, amount, currency)) or not all(x in text for x in (rid, deadline, amount, currency)):
            return False
    return all(x in text for x in ("4", "3", "superior twin", "htl_shinjuku_grand", "htl_myeongdong_plaza"))


CHECKS = [
    ("s8_exact_hotels_reserved", s8_exact_hotels_reserved, 1.5),
    ("s8_booking_register_matches_policies", s8_booking_register_matches_policies, 1.5),
]
