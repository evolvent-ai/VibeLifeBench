from __future__ import annotations

from ._helpers import _tool_call_matches, _workspace_file_text, text_has


def s6_scheduled_monitor_checks_required_states(env) -> bool:
    checks = [
        _tool_call_matches(env, ["weather__get_forecast_daily"], lambda a: str(a.get("geo") or "").lower() == "osaka", 6),
        _tool_call_matches(env, ["flight_booking__search_flights", "flight_booking__list_bookings"], lambda a: "kix" in str(a).lower() or not a, 6),
        _tool_call_matches(env, ["hotel_booking__search_hotels", "hotel_booking__get_hotel_details", "hotel_booking__list_reservations"], lambda a: any(x in str(a).lower() for x in ("osaka", "kyoto", "arima", "jp_ht_")) or not a, 6),
        _tool_call_matches(env, ["visa_and_advisory__check_entry_requirements", "visa_and_advisory__get_advisory"], lambda a: "jp" in str(a).lower(), 6),
    ]
    return sum(bool(x) for x in checks) >= 3


def s6_monitor_result_is_durable(env) -> bool:
    text = _workspace_file_text(env, "decision_log.md") + "\n" + _workspace_file_text(env, "risk_register.md")
    return bool(
        "2026-09-10" in text
        and text_has(text, [["owner", "responsible owner"], ["next review", "next check", "next review date"], ["pending", "open", "awaiting confirmation", "unresolved"]])
    )


CHECKS = [
    ("s6_scheduled_monitor_checks_required_states", s6_scheduled_monitor_checks_required_states, 1.25),
    ("s6_monitor_result_is_durable", s6_monitor_result_is_durable, 1.25),
]
