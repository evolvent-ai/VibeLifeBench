from __future__ import annotations

from ._helpers import calendar_has, health_has, stage_record


def chk_s25_late_digest_screen_breaks(env) -> bool:
    source = health_has(env, ("score",), (("eye_fatigue=5/10",), ("improved_but_persistent",), ("weekend_review_minutes=105",), ("offscreen_rhythm_needed=true",)))
    risk = stage_record(env, "risk_log.md", 25, (("eye fatigue", "5/10"), ("improved", "not fully resolved"), ("screen", "105"), ("screen-free break cadence",)), ("Evidence/source", "Decision", "Activity change"))
    return source and risk and calendar_has(env, (("screen-free", "distance gaze", "eyes-closed rest", "eye break"),))


CHECKS = [("chk_s25_late_digest_screen_breaks", chk_s25_late_digest_screen_breaks, 1.5)]
