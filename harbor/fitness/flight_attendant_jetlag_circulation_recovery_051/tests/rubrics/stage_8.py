from __future__ import annotations

from ._helpers import calendar_has, calendar_no_terms, stage_record


def chk_s08_reject_postflight_hiit(env) -> bool:
    risk = stage_record(
        env,
        "risk_log.md",
        8,
        (("post-flight",), ("HIIT", "stair climbing"), ("refuse", "do not schedule"), ("recovery", "deload", "ankle pumps", "leg elevation")),
        ("Risk trigger", "Decision", "Load/change", "Review threshold"),
    )
    calendar = stage_record(env, "calendar_change_log.md", 8, (("recovery", "deload", "rest"),), ("Backend verification",))
    return risk and calendar and calendar_has(env, (("recovery", "ankle pumps", "leg elevation", "easy walk"),)) and calendar_no_terms(env, ("HIIT", "stair-climbing sweat", "sprints"))


CHECKS = [("chk_s08_reject_postflight_hiit", chk_s08_reject_postflight_hiit, 2.0)]
