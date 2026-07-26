from __future__ import annotations

from ._helpers import payment_status_stage21, persistent_record, ticket_ready_stage27


def r48_final_review_archived(env) -> bool:
    return bool(
        ticket_ready_stage27(env)
        and payment_status_stage21(env)
        and persistent_record(env, 29, "final_review", "复盘", "成绩", min_hits=2)
    )


CHECKS = [
    ("r48_final_review_archived", r48_final_review_archived, 1.5),
]
