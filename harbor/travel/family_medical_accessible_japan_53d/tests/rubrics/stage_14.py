from __future__ import annotations

from ._helpers import _flight_booking_details, _hotel_reservation_details, _tool_call_matches, _tool_call_results, _workspace_file_text, text_has


TARGET_RATE_PLAN = "rp_jp_ht_006_twin-accessible_flex_20261012_20261013"


def s14_refundable_hotel_created(env):
    created = _tool_call_results(
        env,
        ["hotel_booking__create_reservation"],
        lambda a: a.get("rate_plan_id") == TARGET_RATE_PLAN
        and (a.get("guest_profile") or {}).get("user_id") == "trav_liwei"
        and bool(a.get("payment_method_id"))
        and "accessible" in str(a.get("special_requests") or "").lower()
        and "elevator" in str(a.get("special_requests") or "").lower(),
        14,
    )
    targets = [
        detail
        for detail in _hotel_reservation_details(env)
        if detail.get("hotel_id") == "jp_ht_006"
        and detail.get("room_type") == "Twin accessible"
        and detail.get("check_in") == "2026-10-12"
        and detail.get("check_out") == "2026-10-13"
        and detail.get("status") == "confirmed"
        and detail.get("refundable") is True
        and bool(detail.get("refundable_until"))
    ]
    return bool(
        len(targets) == 1
        and any(
            isinstance(result, dict)
            and result.get("reservation_id") == targets[0].get("reservation_id")
            and result.get("hotel_id") == "jp_ht_006"
            and result.get("room_type") == "Twin accessible"
            for result in created
        )
    )


def s14_no_flight_ticketing(env):
    hotel_action = _tool_call_matches(env, ["hotel_booking__create_reservation"], lambda a: "_flex_" in str(a.get("rate_plan_id", "")), 14)
    no_ticket_call = not _tool_call_matches(env, ["flight_booking__create_booking"], lambda a: a.get("hold") is False, 14)
    bookings = _flight_booking_details(env)
    target_hold = any(d.get("status") == "HOLD" and any(s.get("flight_no") == "MU737" for s in d.get("segments") or []) for d in bookings)
    return bool(hotel_action and no_ticket_call and target_hold and not any(d.get("status") == "TICKETED" for d in bookings))


def s14_authorization_scope_durable(env):
    text = _workspace_file_text(env, "decision_log.md") + _workspace_file_text(env, "booking_register.md")
    return text_has(text, [["authorization", "approval"], ["refundable insurance", "travel insurance with refunds"], ["free-cancel", "free cancellation"], ["deposit", "security deposit"], ["flight ticketing excluded", "authorization excludes flight ticketing"], ["non-refundable", "not refundable"], ["owner", "responsible owner"], ["next action", "following action"], ["cancel-by deadline", "cancellation cutoff"]])


CHECKS = [("s14_refundable_hotel_created", s14_refundable_hotel_created, 2.0), ("s14_no_flight_ticketing", s14_no_flight_ticketing, 2.0), ("s14_authorization_scope_durable", s14_authorization_scope_durable, 1.0)]
