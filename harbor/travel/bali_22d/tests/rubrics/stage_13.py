"""Stage 13: verify an exact operational-status lookup for the ticketed outbound."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import _call, _tool_call_matches, list_flight_bookings


def _outbound_flight_no(env) -> str | None:
    for booking in list_flight_bookings(env):
        if str(booking.get("status") or "").upper() != "TICKETED":
            continue
        for segment in booking.get("segments") or []:
            if not isinstance(segment, dict):
                continue
            if (
                str(segment.get("origin") or "").upper() == "PVG"
                and str(segment.get("destination") or segment.get("dest") or "").upper() == "DPS"
                and str(segment.get("depart_dt") or "")[:10] == "2026-06-10"
            ):
                return str(segment.get("flight_no") or "").strip()
    return None


def s13_exact_flight_status_checked(env) -> bool:
    flight_no = _outbound_flight_no(env)
    if not flight_no:
        logger.info("s13_exact_flight_status_checked: FAIL -- no ticketed outbound")
        return False
    queried = _tool_call_matches(
        env,
        "flight_booking",
        "get_flight_status",
        lambda a: str(a.get("flight_no") or "").replace(" ", "").upper() == flight_no.replace(" ", "").upper()
        and str(a.get("date") or "") == "2026-06-10",
        stage=13,
    )
    if not queried:
        return False
    status = _call(env, "flight_booking", "get_flight_status", flight_no=flight_no, date="2026-06-10")
    result = (
        isinstance(status, dict)
        and str(status.get("flight_no") or "").replace(" ", "").upper() == flight_no.replace(" ", "").upper()
        and str(status.get("status") or "").upper() == "ARRIVED"
        and str(status.get("actual_arrive") or "") == "2026-06-10T12:18:00+08:00"
        and str(status.get("gate") or "").upper() == "B4"
        and int(status.get("delay_min") or 0) == 3
    )
    logger.info("s13_exact_flight_status_checked: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [("s13_exact_flight_status_checked", s13_exact_flight_status_checked, 2.0)]
