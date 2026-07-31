from __future__ import annotations

from ._helpers import course_order_complete, persistent_record


def r42_mock_feedback_adapted(env) -> bool:
    return bool(
        course_order_complete(env)
        and persistent_record(env, 25, "药学综合", "法规", "不通宵", min_hits=2)
    )


CHECKS = [
    ("r42_mock_feedback_adapted", r42_mock_feedback_adapted, 1.5),
]
