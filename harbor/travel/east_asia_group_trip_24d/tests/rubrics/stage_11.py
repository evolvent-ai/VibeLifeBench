"""Stage 11: verify MU501 is no longer active and a real replacement arrives before the fixed meeting."""
from __future__ import annotations

from loguru import logger

from ._helpers import _flight_booking_details, _tool_calls, _tool_name_matches, _workspace_file_text

_ACTIVE = {"TICKETED", "HOLD", "CONFIRMED"}


def _segments(booking: dict):
    return [s for s in booking.get("segments") or [] if isinstance(s, dict)]


def _mu501_active(booking: dict) -> bool:
    if str(booking.get("status") or "").upper() not in _ACTIVE:
        return False
    return any(str(s.get("flight_no") or "").replace(" ", "").upper() == "MU501" and str(s.get("depart_dt") or "")[:10] == "2026-06-05" for s in _segments(booking))


def _replacement(env) -> tuple[dict, dict] | None:
    for booking in _flight_booking_details(env):
        if str(booking.get("status") or "").upper() != "TICKETED":
            continue
        for segment in _segments(booking):
            no = str(segment.get("flight_no") or "").replace(" ", "").upper()
            origin = str(segment.get("origin") or "").upper()
            dest = str(segment.get("destination") or segment.get("dest") or "").upper()
            arrival = str(segment.get("arrive_dt") or "")
            if no != "MU501" and origin in {"PVG", "SHA"} and dest in {"NRT", "HND"} and arrival[:10] <= "2026-06-05":
                return booking, segment
    return None


def s11_cancelled_flight_was_verified(env) -> bool:
    calls = _tool_calls(env, 11)
    verified = any(
        _tool_name_matches(str(call.get("name") or ""), "flight_booking", "get_flight_status")
        and isinstance(call.get("arguments"), dict)
        and str(call["arguments"].get("flight_no") or "").replace(" ", "").upper() == "MU501"
        and str(call["arguments"].get("date") or "") == "2026-06-05"
        for call in calls
    )
    recovery_write = any(
        _tool_name_matches(str(call.get("name") or ""), "flight_booking", tool)
        for call in calls for tool in ("change_booking", "create_booking", "cancel_booking")
    )
    bookings = _flight_booking_details(env)
    result = verified and recovery_write and not any(_mu501_active(b) for b in bookings)
    logger.info("s11_cancelled_flight_was_verified: {}", "PASS" if result else "FAIL")
    return result


def s11_replacement_arrives_before_meeting_day(env) -> bool:
    replacement = _replacement(env)
    if not replacement:
        return False
    booking, segment = replacement
    text = (_workspace_file_text(env, "/workspace/bookings.md") + "\n" + _workspace_file_text(env, "/workspace/incident_log.md") + "\n" + _workspace_file_text(env, "/workspace/budget.md")).casefold()
    pnr = str(booking.get("pnr") or "").casefold()
    flight_no = str(segment.get("flight_no") or "").casefold()
    amount = booking.get("paid_amount") or (booking.get("total_paid") or {}).get("amount")
    currency = booking.get("currency") or (booking.get("total_paid") or {}).get("currency")
    result = bool(
        pnr and pnr in text and flight_no and flight_no in text
        and "mu501" in text and "cancelled" in text
        and str(segment.get("arrive_dt") or "")[:10] in text
        and any(x in text for x in ("2026-06-06", "6/6", "meeting"))
        and amount is not None and str(amount) in text and str(currency or "").casefold() in text
    )
    logger.info("s11_replacement_arrives_before_meeting_day: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [
    ("s11_cancelled_flight_was_verified", s11_cancelled_flight_was_verified, 2.0),
    ("s11_replacement_arrives_before_meeting_day", s11_replacement_arrives_before_meeting_day, 3.5),
]
