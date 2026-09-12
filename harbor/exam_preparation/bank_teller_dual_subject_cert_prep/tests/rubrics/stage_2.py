from __future__ import annotations
from . import _helpers as h


def r05_initial_calendar_no_conflict(env) -> bool:
    return bool(
        h.tool_used(env, 2, "calendar")
        and h.calendar_has_baseline_constraints(env)
        and h.durable_evidence_contains(
            env, "study plan", "study_plan.md",
            ("临柜", "排班"), ("培训", "新柜员课程"), ("扎账", "结账"), ("避开", "冲突"),
        )
    )


CHECKS = [("r05_initial_calendar_no_conflict", r05_initial_calendar_no_conflict, 1.25)]
