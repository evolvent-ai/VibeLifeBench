from __future__ import annotations

from ._helpers import health_has, stage_record


def chk_s01_health_baseline_recorded(env) -> bool:
    source = health_has(env, ("steps", "sleep_minutes", "score"), (("4180",), ("6.0h",), ("neck_stiffness=3/10",), ("eye_fatigue=6/10",)))
    recorded = stage_record(env, "risk_log.md", 1, (("4180",), ("6.0", "360"), ("neck", "3/10"), ("eye fatigue", "6/10")), ("Evidence/source", "Severity", "Status"))
    return source and recorded


def chk_s01_safety_thresholds_defined(env) -> bool:
    return stage_record(env, "risk_log.md", 1, (("neck", "4/10"), ("eye fatigue", "7/10"), ("pain", "forceful traction"), ("professional evaluation",), ("de-load", "pause")), ("Decision", "Activity change", "Review threshold"))


CHECKS = [
    ("chk_s01_health_baseline_recorded", chk_s01_health_baseline_recorded, 1.5),
    ("chk_s01_safety_thresholds_defined", chk_s01_safety_thresholds_defined, 2.0),
]
