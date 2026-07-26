from __future__ import annotations

from . import _backend_checks as backend


def final_route_and_deadline_closed(env) -> bool:
    return backend.safe_ticketed_route_complete(env) and backend.required_travelers_ticketed(env) and backend.registration_calendar_ready(env)


def final_hotel_and_transfer_closed(env) -> bool:
    return backend.lodging_complete(env) and backend.hotel_authorization_integrity(env) and backend.map_transfer_route_available(env)


def final_payment_and_receipts_consistent(env) -> bool:
    return backend.payment_state_consistent(env) and backend.budget_split_recorded(env) and backend.receipts_matrix_recorded(env)


def final_archive_backend_consistent(env) -> bool:
    return backend.final_summary_backend_consistent(env) and backend.persistent_artifacts_complete(env) and backend.organizer_confirmation_sent(env)


CHECKS = [
    ("final_route_and_deadline_closed", final_route_and_deadline_closed, 3.0),
    ("final_hotel_and_transfer_closed", final_hotel_and_transfer_closed, 3.0),
    ("final_payment_and_receipts_consistent", final_payment_and_receipts_consistent, 3.0),
    ("final_archive_backend_consistent", final_archive_backend_consistent, 3.0),
]
