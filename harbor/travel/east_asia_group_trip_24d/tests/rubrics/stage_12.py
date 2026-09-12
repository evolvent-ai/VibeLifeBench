"""Stage 12: recheck real room availability and bind the incident to an affected reservation state."""
from __future__ import annotations

from loguru import logger

from ._helpers import _call, _hotel_reservation_details, _tool_calls, _tool_name_matches, _workspace_file_text


def _uses(env, tool: str) -> bool:
    return any(
        _tool_name_matches(str(c.get("name") or ""), "hotel_booking", tool)
        and isinstance(c.get("arguments"), dict)
        and c["arguments"].get("hotel_id") == "htl_shinjuku_grand"
        for c in _tool_calls(env, 12)
    )


def _actual_state(env) -> tuple[bool, list[dict]]:
    availability = _call(env, "hotel_booking", "get_room_availability", hotel_id="htl_shinjuku_grand", check_in="2026-06-05", check_out="2026-06-08", guests=2)
    rows = availability.get("rooms", availability.get("items", [])) if isinstance(availability, dict) else availability
    if not isinstance(rows, list):
        raise ValueError("hotel_booking.get_room_availability returned invalid payload")
    room_names = {str(r.get("room_type") or "").casefold() for r in rows if isinstance(r, dict)}
    reservations = _hotel_reservation_details(env)
    affected = [r for r in reservations if r.get("hotel_id") == "htl_shinjuku_grand" and r.get("room_type") == "Superior Twin" and str(r.get("check_in"))[:10] == "2026-06-05" and str(r.get("check_out"))[:10] == "2026-06-08" and str(r.get("status") or "").casefold() == "walked"]
    return "superior twin" not in room_names and "standard twin" in room_names, affected


def s12_shinjuku_inventory_rechecked(env) -> bool:
    if _uses(env, "get_room_availability"):
        unavailable, affected = _actual_state(env)
        result = unavailable and bool(affected)
    else:
        # Backward-compatible judge fixture path; production trajectory uses the availability branch above.
        used = _uses(env, "get_hotel_details")
        detail = _call(env, "hotel_booking", "get_hotel_details", hotel_id="htl_shinjuku_grand") if used else {}
        blob = str(detail).casefold()
        result = used and all(x in blob for x in ("superior twin", "sold_out", "2026-06-05", "2026-06-07"))
    logger.info("s12_shinjuku_inventory_rechecked: {}", "PASS" if result else "FAIL")
    return result


def s12_recovery_record_is_durable(env) -> bool:
    incident = _workspace_file_text(env, "/workspace/incident_log.md").casefold()
    bookings = _workspace_file_text(env, "/workspace/bookings.md").casefold()
    if _uses(env, "get_room_availability"):
        unavailable, affected = _actual_state(env)
        ids = [str(r.get("reservation_id") or "").casefold() for r in affected]
        object_ok = unavailable and bool(ids) and all(rid and rid in incident + "\n" + bookings for rid in ids)
    else:
        object_ok = "htl_shinjuku_grand" in incident + bookings
    result = bool(
        object_ok and all(x in incident for x in ("superior twin", "2026-06-05", "2026-06-07"))
        and any(x in incident for x in ("sold_out", "walked"))
        and "owner" in incident
        and any(x in incident for x in ("next action", "replacement"))
        and any(x in bookings for x in ("affected", "walked"))
        and "superior twin confirmed" not in bookings
    )
    return result


CHECKS = [
    ("s12_shinjuku_inventory_rechecked", s12_shinjuku_inventory_rechecked, 1.5),
    ("s12_recovery_record_is_durable", s12_recovery_record_is_durable, 1.5),
]
