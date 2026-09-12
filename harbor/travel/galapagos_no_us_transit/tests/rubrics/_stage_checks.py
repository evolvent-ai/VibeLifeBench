from __future__ import annotations

from . import _backend_checks as backend
from ._helpers import contains_all_groups, read_file, workspace_text


def _persistent(env, groups) -> bool:
    return contains_all_groups(workspace_text(env), groups)


def s0(env) -> bool:
    return backend.persistent_artifacts_complete(env) and _persistent(
        env, [["LIN QIAO", "passport name is Lin Qiao"], ["XU WEN CHENG", "Xu Wen Cheng"], ["seasick", "seasickness"], ["approval", "authorization", "permission"]]
    )


def s1(env) -> bool:
    return backend.registration_calendar_ready(env) and backend.map_transfer_route_available(env)


def s2(env) -> bool:
    return backend.travel_window_calendar_ready(env)


def s3(env) -> bool:
    return backend.organizer_source_ingested(env)


def s4(env) -> bool:
    return _persistent(
        env, [["US", "United States", "no-US"], ["transit", "connection"], ["budget", "budget"], ["private", "personal"]]
    )


def s5(env) -> bool:
    return backend.all_active_bookings_avoid_us(env) and _persistent(
        env, [["no US", "no-US transit", "no-US"], ["registration", "check-in"], ["buffer", "hold"]]
    )


def s6(env) -> bool:
    return backend.safe_outbound_held_or_ticketed(env)


def s7(env) -> bool:
    return backend.lodging_complete(env) and backend.hotel_authorization_integrity(env)


def s8(env) -> bool:
    return backend.weather_risk_available(env) and _persistent(
        env, [["ash", "ash warning"], ["rechecked", "recheck"], ["route", "itinerary"]]
    )


def s9(env) -> bool:
    return backend.safe_outbound_held_or_ticketed(env) and _persistent(
        env, [["waiver", "exception"], ["rechecked", "verification"], ["registration", "check-in"]]
    )


def s10(env) -> bool:
    return backend.hotel_authorization_integrity(env) and _persistent(
        env, [["Puerto Ayora"], ["refundable", "free cancellation"], ["hotel", "lodging"]]
    )


def s11(env) -> bool:
    return backend.safe_outbound_held_or_ticketed(env) and backend.hotel_authorization_integrity(env)


def s12(env) -> bool:
    return backend.passport_names_match(env)


def s13(env) -> bool:
    return backend.weather_risk_available(env) and backend.map_transfer_route_available(env) and _persistent(
        env, [["seasick", "seasickness"], ["land activity", "shore transect"], ["swell", "sea state", "sea conditions"]]
    )


def s14(env) -> bool:
    return backend.budget_split_recorded(env)


def s15(env) -> bool:
    return backend.transfer_calendar_ready(env) and _persistent(
        env, [["GPS", "Baltra"], ["Puerto Ayora"], ["buffer", "backup"]]
    )


def s16(env) -> bool:
    return backend.safe_ticketed_route_complete(env) and backend.lodging_complete(env)


def s17(env) -> bool:
    return backend.payment_state_consistent(env)


def s18(env) -> bool:
    return backend.registration_calendar_ready(env) and backend.travel_window_calendar_ready(env) and backend.transfer_calendar_ready(env)


def s19(env) -> bool:
    return backend.departure_status_rechecked(env) and _persistent(
        env, [["delay", "disruption", "ash", "ash warning"], ["rechecked", "recheck"]]
    )


def s20(env) -> bool:
    return backend.safe_ticketed_route_complete(env) and _persistent(
        env, [["actual", "arrival time"], ["arrival", "arrival point", "Puerto Ayora"], ["status", "status", "archive", "state"]]
    )


def s21(env) -> bool:
    return backend.registration_calendar_ready(env) and backend.organizer_confirmation_sent(env) and backend.map_transfer_route_available(env)


def s22(env) -> bool:
    return backend.weather_risk_available(env) and backend.weather_calendar_updated(env)


def s23(env) -> bool:
    return backend.receipts_matrix_recorded(env) and backend.return_single_ticket_complete(env)


def s24(env) -> bool:
    return backend.final_summary_backend_consistent(env)


CHECK_FUNCTIONS = {
    0: s0, 1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8,
    9: s9, 10: s10, 11: s11, 12: s12, 13: s13, 14: s14, 15: s15,
    16: s16, 17: s17, 18: s18, 19: s19, 20: s20, 21: s21, 22: s22,
    23: s23, 24: s24,
}


def run_stage(env, stage: int) -> bool:
    previous = getattr(env, "current_stage", None)
    env.current_stage = stage
    try:
        return bool(CHECK_FUNCTIONS[stage](env))
    finally:
        env.current_stage = previous
