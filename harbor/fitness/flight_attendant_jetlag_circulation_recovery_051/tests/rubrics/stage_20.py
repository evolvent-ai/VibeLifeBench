from __future__ import annotations

from ._helpers import calendar_has, calendar_no_terms, health_has, stage_record, stage_service_count


def chk_s20_longhaul_recovery(env) -> bool:
    observed = health_has(env, ("steps", "score"), (("longhaul",), ("fatigue=7/10",), ("recovery_priority=high",)))
    risk = stage_record(
        env,
        "risk_log.md",
        20,
        (("New York", "JFK"), ("long-haul",), ("24 hours", "24h"), ("recovery-first",), ("no high intensity", "deload")),
        ("Evidence/source", "Load/change", "Review threshold"),
    )
    return observed and risk and calendar_has(env, (("recovery", "rest", "light activity"),)) and calendar_no_terms(env, ("HIIT", "sprints", "high-intensity leg training"))


def chk_s20_recovery_light_refresh(env) -> bool:
    return stage_record(env, "stage_progress.md", 20, (("health",), ("personal calendar", "calendar"), ("recorded and reviewed", "verified")), ("Facts read", "Action/result")) and stage_service_count(env, 20, ("health_tracker", "calendar")) == 2


CHECKS = [
    ("chk_s20_longhaul_recovery", chk_s20_longhaul_recovery, 1.75),
    ("chk_s20_recovery_light_refresh", chk_s20_recovery_light_refresh, 1.0),
]
