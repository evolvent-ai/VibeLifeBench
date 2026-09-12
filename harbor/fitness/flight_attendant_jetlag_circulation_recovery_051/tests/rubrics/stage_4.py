from __future__ import annotations

from ._helpers import calendar_has, calendar_no_terms, notion_has, stage_record


def chk_s04_low_impact_plan(env) -> bool:
    plan = calendar_has(env, (("low-impact", "recovery"), ("brisk walking", "elliptical", "yoga"), ("light strength",), ("post-flight", "after flight")))
    logged = stage_record(
        env,
        "calendar_change_log.md",
        4,
        (("low-impact",), ("brisk walking", "elliptical", "yoga"), ("light strength",), ("post-flight", "recovery")),
        ("Calendar object", "New window", "Backend verification"),
    )
    return plan and logged and calendar_no_terms(env, ("HIIT", "stair sprints", "hard leg-slimming training")) and notion_has(env, "cross-time-zone recovery training control center", (("recovery",),))


def chk_s04_metric_logging_plan(env) -> bool:
    return stage_record(
        env,
        "risk_log.md",
        4,
        (("record",), ("sleep",), ("rpe",), ("swelling",), ("fatigue",), ("missing", "unknown", "not_observed")),
        ("Evidence/source", "Load/change", "Review threshold"),
    )


CHECKS = [
    ("chk_s04_low_impact_plan", chk_s04_low_impact_plan, 1.75),
    ("chk_s04_metric_logging_plan", chk_s04_metric_logging_plan, 1.25),
]
