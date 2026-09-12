from __future__ import annotations
from . import _helpers as h


def r40_no_overnight_cram(env) -> bool:
    return bool(
        h.tool_used(env, 22, "calendar")
        and h.calendar_has_exam_day_plan(env)
        and h.calendar_has_no_overnight_study(env)
        and h.durable_evidence_contains(
            env, "pre exam checklist", "pre_exam_checklist.md",
            "2026-08-15", "22:30", ("停止复习", "睡眠"), ("出发", "缓冲"),
        )
    )


CHECKS = [("r40_no_overnight_cram", r40_no_overnight_cram, 2.0)]
