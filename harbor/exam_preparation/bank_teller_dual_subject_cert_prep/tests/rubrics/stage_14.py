from __future__ import annotations
from . import _helpers as h


def r28_calendar_change_logged(env) -> bool:
    return bool(
        h.tool_used(env, 14, "calendar")
        and h.any_tool(env, 14, ("notion",))
        and h.calendar_has_marketing_reschedule(env)
        and h.durable_evidence_contains(
            env, "calendar change", "calendar_change_log.md",
            "2026-07-26", "2026-07-28", ("营销", "社区"), "取消", ("新时间", "改期"),
        )
    )


CHECKS = [("r28_calendar_change_logged", r28_calendar_change_logged, 1.25)]
