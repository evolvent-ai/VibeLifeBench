"""Stage 14: require a successful OZ102 check-in result and persist the returned boarding objects."""
from __future__ import annotations

from loguru import logger

from ._helpers import _flight_booking_details, _tool_calls, _tool_name_matches, _tool_result_text, _workspace_file_text


def s14_gate(env) -> bool:
    calls = [c for c in _tool_calls(env, 14) if _tool_name_matches(str(c.get("name") or ""), "flight_booking", "check_in")]
    if len(calls) != 1:
        return False
    call = calls[0]
    args = call.get("arguments") if isinstance(call.get("arguments"), dict) else {}
    pnr = str(args.get("pnr") or "")
    try:
        segment_idx = int(args.get("segment_idx"))
    except (TypeError, ValueError):
        return False
    booking = next((b for b in _flight_booking_details(env) if str(b.get("pnr") or "") == pnr), None)
    if not booking:
        return False
    segments = [s for s in booking.get("segments") or [] if isinstance(s, dict)]
    if not 0 <= segment_idx < len(segments):
        return False
    segment = segments[segment_idx]
    exact_segment = str(segment.get("flight_no") or "").replace(" ", "").upper() == "OZ102" and str(segment.get("depart_dt") or "")[:10] == "2026-06-08"
    result_text = _tool_result_text(call)
    success_result = call.get("success") is True and any(x in result_text for x in ("boarding_pass", "boarding pass", "seat", "checked_in", "check-in complete"))
    bookings = _workspace_file_text(env, "/workspace/bookings.md").casefold()
    result_objects = [token for token in result_text.replace('"', ' ').replace("'", " ").split() if "bp-" in token or "boarding" in token]
    persisted = pnr.casefold() in bookings and "oz102" in bookings and any(x in bookings for x in ("boarding", "seat"))
    if result_objects:
        persisted = persisted and any(obj.strip(" ,:[]{}") in bookings for obj in result_objects)
    ok = bool(exact_segment and success_result and persisted)
    logger.info("s14_gate: exact_segment={} result={} persisted={} -> {}", exact_segment, success_result, persisted, "PASS" if ok else "FAIL")
    return ok


CHECKS = [("s14_gate", s14_gate, 2)]
