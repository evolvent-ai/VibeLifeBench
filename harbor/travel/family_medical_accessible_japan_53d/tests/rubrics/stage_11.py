from __future__ import annotations

from ._helpers import _call_json, _flight_booking_details, _tool_call_matches, _workspace_file_text, text_has

OID = "of_kansai_daytime_refundable_hold"


def s11_extension_rechecked(env):
    detail = _call_json(env, "flight_booking", "get_flight_offer", offer_id=OID)
    return _tool_call_matches(env, ["flight_booking__get_flight_offer"], lambda a: a.get("offer_id") == OID, 11) and detail.get("expires_at") == "2026-09-19T16:00:00+08:00"


def s11_no_ticketing(env):
    authorized_action = _tool_call_matches(env, ["flight_booking__get_flight_offer"], lambda a: a.get("offer_id") == OID, 11)
    no_ticket_call = not _tool_call_matches(env, ["flight_booking__create_booking"], lambda a: a.get("hold") is False, 11)
    bookings = _flight_booking_details(env)
    target_hold = any(d.get("status") == "HOLD" and any(s.get("flight_no") == "MU737" for s in d.get("segments") or []) for d in bookings)
    return bool(authorized_action and no_ticket_call and target_hold and not any(d.get("status") == "TICKETED" for d in bookings))


def s11_durable(env):
    return text_has(_workspace_file_text(env, "booking_register.md"), [[OID], ["2026-09-19"], ["not ticketed", "ticket not issued"], ["not charged", "not paid"], ["vendor", "travel supplier"]])


CHECKS = [("s11_extension_rechecked", s11_extension_rechecked, 1.0), ("s11_no_ticketing", s11_no_ticketing, 0.5), ("s11_durable", s11_durable, 0.5)]
