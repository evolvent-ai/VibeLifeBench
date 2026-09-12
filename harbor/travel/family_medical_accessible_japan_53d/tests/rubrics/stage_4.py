from __future__ import annotations

from ._helpers import _call_json, _tool_call_matches, _workspace_file_text, text_has

HOTEL_ID = "jp_ht_001"


def s4_checks_accessible_hotels(env) -> bool:
    searched = _tool_call_matches(
        env,
        ["hotel_booking__search_hotels", "hotel_booking__get_hotel_details"],
        lambda a: HOTEL_ID == a.get("hotel_id") or "kyoto" in str(a).lower(),
        stage=4,
    )
    availability_call = _tool_call_matches(
        env,
        ["hotel_booking__get_room_availability"],
        lambda a: a.get("hotel_id") == HOTEL_ID
        and a.get("check_in") == "2026-10-15"
        and a.get("check_out") == "2026-10-16"
        and int(a.get("guests") or 0) == 2,
        stage=4,
    )
    rows = _call_json(
        env,
        "hotel_booking",
        "get_room_availability",
        hotel_id=HOTEL_ID,
        check_in="2026-10-15",
        check_out="2026-10-16",
        guests=2,
    )
    backend = any(
        isinstance(row, dict)
        and row.get("flavor") == "flex"
        and row.get("inventory_remaining") == 1
        and 21450 in (row.get("nightly_prices") or [])
        and row.get("currency") == "JPY"
        and row.get("refundable") is True
        for row in (rows if isinstance(rows, list) else [])
    )
    durable = text_has(
        _workspace_file_text(env, "trip_plan.md") + _workspace_file_text(env, "decision_log.md"),
        [[HOTEL_ID], ["21450", "21,450"], ["jpy"], ["inventory 1", "one room in inventory", "only 1 left"], ["accessible", "accessible room"], ["refundable", "free cancellation"]],
    )
    return bool(searched and availability_call and backend and durable)


CHECKS = [("s4_checks_accessible_hotels", s4_checks_accessible_hotels, 2.0)]
