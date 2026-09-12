from __future__ import annotations

from . import _backend_checks as backend


def cross_all_active_bookings_no_us(env) -> bool:
    return backend.safe_ticketed_route_complete(env) and backend.all_active_bookings_avoid_us(env)


def cross_single_ticket_and_travelers(env) -> bool:
    return backend.outbound_single_ticket_complete(env) and backend.return_single_ticket_complete(env) and backend.required_travelers_ticketed(env)


def cross_hotel_authorization_integrity(env) -> bool:
    return backend.lodging_complete(env) and backend.hotel_authorization_integrity(env)


def cross_calendar_deadline_continuity(env) -> bool:
    return backend.registration_calendar_ready(env) and backend.travel_window_calendar_ready(env) and backend.transfer_calendar_ready(env)


def cross_organizer_communication(env) -> bool:
    return backend.organizer_source_ingested(env) and backend.organizer_confirmation_sent(env)


def cross_budget_payment_consistency(env) -> bool:
    return backend.budget_split_recorded(env) and backend.payment_state_consistent(env)


def cross_weather_transfer_recovery(env) -> bool:
    return backend.weather_risk_available(env) and backend.map_transfer_route_available(env) and backend.weather_calendar_updated(env)


def cross_persistent_archive_completeness(env) -> bool:
    return backend.persistent_artifacts_complete(env) and backend.receipts_matrix_recorded(env)


CHECKS = [
    ("cross_all_active_bookings_no_us", cross_all_active_bookings_no_us, 4.0),
    ("cross_single_ticket_and_travelers", cross_single_ticket_and_travelers, 4.0),
    ("cross_hotel_authorization_integrity", cross_hotel_authorization_integrity, 4.0),
    ("cross_calendar_deadline_continuity", cross_calendar_deadline_continuity, 4.0),
    ("cross_organizer_communication", cross_organizer_communication, 3.0),
    ("cross_budget_payment_consistency", cross_budget_payment_consistency, 3.0),
    ("cross_weather_transfer_recovery", cross_weather_transfer_recovery, 3.0),
    ("cross_persistent_archive_completeness", cross_persistent_archive_completeness, 3.0),
]
