"""Stage 22: bind the ash contingency to the live alert and actual return booking."""
from __future__ import annotations

from .shared._helpers import _call, _tool_call_matches, list_flight_bookings, workspace_file_content


def _return_object(env) -> tuple[dict, str, str, int] | None:
    for booking in list_flight_bookings(env):
        if str(booking.get("status") or "").upper() not in {"TICKETED", "CHECKED_IN"}:
            continue
        for segment in booking.get("segments") or []:
            if isinstance(segment, dict) and str(segment.get("origin") or "").upper() == "DPS" and str(segment.get("destination") or segment.get("dest") or "").upper() == "PVG" and str(segment.get("depart_dt") or "")[:10] == "2026-07-01":
                return booking, str(booking.get("pnr") or ""), str(segment.get("flight_no") or ""), int(segment.get("segment_idx") or 0)
    return None


def s22_ash_contingency_plan(env) -> bool:
    obj = _return_object(env)
    if not obj:
        return False
    booking, pnr, flight_no, segment_idx = obj
    passengers = booking.get("passengers")
    if not isinstance(passengers, list) or not passengers:
        return False
    checkin_called = _tool_call_matches(
        env,
        "flight_booking",
        "check_in",
        lambda a: str(a.get("pnr") or "") == pnr
        and int(a.get("segment_idx") or 0) == segment_idx
        and (
            a.get("pax_indices") is None
            or set(a.get("pax_indices") or []) == set(range(len(passengers)))
        ),
        stage=22,
    )
    checked_in = any(
        isinstance(item, dict)
        and str(item.get("event") or "").upper() == "CHECKED_IN"
        and f"segment={segment_idx}" in str(item.get("detail") or "")
        for item in booking.get("history") or []
    )
    status_checked = _tool_call_matches(
        env,
        "flight_booking",
        "get_flight_status",
        lambda a: str(a.get("flight_no") or "").replace(" ", "").upper() == flight_no.replace(" ", "").upper() and str(a.get("date") or "") == "2026-07-01",
        stage=22,
    )
    ash_checked = _tool_call_matches(
        env,
        "weather",
        "get_alerts",
        lambda a: "bali_dps" in str(a.get("geo") or "").casefold(),
        stage=22,
    )
    alerts = _call(env, "weather", "get_alerts", geo="bali_dps")
    alert_blob = str(alerts).casefold()
    live_alert = "alert_ash_dps_20260629" in alert_blob and "volcanic_ash" in alert_blob and "medium" in alert_blob
    text = (workspace_file_content(env, "/workspace/itinerary.md") + "\n" + workspace_file_content(env, "/workspace/risk_register.md") + "\n" + workspace_file_content(env, "/workspace/HEARTBEAT.md")).casefold()
    object_bound = pnr.casefold() in text and flight_no.casefold() in text and "2026-07-01" in text
    contingency = any(x in text for x in ("alternative flight", "alternative flight", "rebook", "rebook")) and any(x in text for x in ("hotel extension", "extra night"))
    trigger = any(x in text for x in ("airport closure", "closed", "cancelled", "cancel")) and any(x in text for x in ("owner", "owner"))
    return bool(checkin_called and checked_in and status_checked and ash_checked and live_alert and object_bound and contingency and trigger)


CHECKS = [("s22_ash_contingency_plan", s22_ash_contingency_plan, 2.5)]
