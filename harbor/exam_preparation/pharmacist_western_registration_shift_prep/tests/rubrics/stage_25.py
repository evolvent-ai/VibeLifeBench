from __future__ import annotations

from ._helpers import course_order_complete, persistent_record


def r42_feedback_adapted(env) -> bool:
    return bool(
        course_order_complete(env)
        and persistent_record(env, 25, "Comprehensive Pharmacy", "regulations", "no all-nighters", min_hits=2)
    )


CHECKS = [
    ("r42" + "_" + "mock_feedback_adapted", r42_feedback_adapted, 1.5),
]
