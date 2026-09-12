from __future__ import annotations

from ._helpers import health_has, stage_record


def chk_s14_progress_digest(env) -> bool:
    source = health_has(env, ("score",), (("completed_recovery_sessions=5",), ("planned_sessions=7",), ("median_rpe=3/10",), ("calf_edema_trend=improving",), ("deload_count=1",)))
    recorded = stage_record(
        env,
        "stage_progress.md",
        14,
        (("completion", "5/7"), ("rpe", "3/10"), ("swelling",), ("decrease", "improving", "trend"), ("deload reason", "deload")),
        ("Facts read", "Decision", "Action/result"),
    )
    return source and recorded


CHECKS = [("chk_s14_progress_digest", chk_s14_progress_digest, 1.25)]
