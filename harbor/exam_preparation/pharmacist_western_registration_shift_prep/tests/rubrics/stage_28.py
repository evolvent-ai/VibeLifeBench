from __future__ import annotations

from ._helpers import calendar_event_seen, persistent_record, ticket_ready_stage27


def r46_final_checklist_complete(env) -> bool:
    return bool(
        ticket_ready_stage27(env)
        and calendar_event_seen(
            env,
            "licensed pharmacist",
            "City Vocational Education Center A Building",
            date="2026-10-11",
        )
        and persistent_record(env, 28, "12-08", "identity documents", "route", min_hits=2)
    )


def r47_no_overnight_cram(env) -> bool:
    return bool(
        ticket_ready_stage27(env)
        and persistent_record(env, 28, "rest", "no all-nighters", "sleep", min_hits=1)
    )


CHECKS = [
    ("r46_final_checklist_complete", r46_final_checklist_complete, 1.5),
    ("r47_no_overnight_cram", r47_no_overnight_cram, 1.0),
]
