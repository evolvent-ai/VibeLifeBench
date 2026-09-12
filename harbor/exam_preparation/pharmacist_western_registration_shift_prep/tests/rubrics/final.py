from __future__ import annotations

from ._helpers import (
    calendar_event_seen,
    payment_status_stage21,
    persistent_record,
    ticket_ready_stage27,
)


def final_exam_day_synced(env) -> bool:
    return bool(
        ticket_ready_stage27(env)
        and calendar_event_seen(
            env,
            "licensed pharmacist",
            "City Vocational Education Center A Building",
            date="2026-10-11",
        )
        and persistent_record(env, 28, "12-08", "City Vocational Education Center A Building", min_hits=1)
    )


def final_handoff_artifacts_present(env) -> bool:
    return bool(
        payment_status_stage21(env)
        and persistent_record(
            env,
            29,
            "final_review",
            "registration",
            "course",
            "risk",
            "calendar",
            "admission ticket",
            min_hits=4,
        )
    )


CHECKS = [
    ("final_exam_day_synced", final_exam_day_synced, 2.0),
    ("final_handoff_artifacts_present", final_handoff_artifacts_present, 1.5),
]
