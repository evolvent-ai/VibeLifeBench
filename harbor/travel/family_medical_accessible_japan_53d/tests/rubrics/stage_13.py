from __future__ import annotations

from ._helpers import _rows, _tool_call_results, _workspace_file_text, text_has

HOTEL_ID = "jp_ht_006"
DEADLINE = "2026-09-28T23:59:00+09:00"


def s13_hotel_policy_refresh(env) -> bool:
    hotel_results = _tool_call_results(
        env,
        ["hotel_booking__get_hotel_details"],
        lambda a: a.get("hotel_id") == HOTEL_ID,
        stage=13,
    )
    availability_results = _tool_call_results(
        env,
        ["hotel_booking__get_room_availability"],
        lambda a: a.get("hotel_id") == HOTEL_ID and a.get("check_in") == "2026-10-12" and a.get("check_out") == "2026-10-13" and int(a.get("guests") or 0) == 3,
        stage=13,
    )
    hotel_ok = any(
        isinstance(hotel, dict)
        and hotel.get("hotel_id") == HOTEL_ID
        and isinstance(hotel.get("policies"), dict)
        and hotel["policies"].get("free_cancel") == DEADLINE
        and hotel["policies"].get("accessible_inventory_remaining") == 1
        for hotel in hotel_results
    )
    availability_ok = any(
        row.get("rate_plan_id") == "rp_jp_ht_006_twin-accessible_flex_20261012_20261013"
        and row.get("room_type") == "Twin accessible"
        and row.get("flavor") == "flex"
        and row.get("inventory_remaining") == 1
        and row.get("refundable_until") == DEADLINE
        for result in availability_results
        for row in _rows(result, "rate_plans", "results")
    )
    durable = text_has(_workspace_file_text(env, "booking_register.md"), [[HOTEL_ID], [DEADLINE], ["inventory 1", "inventory 1", "inventory 1"], ["accessible", "accessible room"], ["cancel", "cancellation"]])
    return bool(hotel_ok and availability_ok and durable)


CHECKS = [("s13_hotel_policy_refresh", s13_hotel_policy_refresh, 2.0)]
