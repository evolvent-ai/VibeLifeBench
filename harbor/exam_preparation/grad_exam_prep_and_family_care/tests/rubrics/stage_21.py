from __future__ import annotations
from ._helpers import *


def r38_day_two_exam_confirmed_without_new_study_load(env) -> bool:
    try:
        calendar = _calendar_text(env)
        durable = wfile(env, "CONTROL_CENTER.md")
        return (
            _stage_trace_all(env, 21, [["calendar"], ["list_events"], ["notion"], ["api-patch-block-children"]])
            and count_hits(calendar + "\n" + durable, [["2026-12-21", "12-21", "second day"], ["exam", "exam room"], ["no new", "stopstudy", "do not add tasks"]]) == 3
            and calendar_has_no_long_study_blocks(env)
        )
    except Exception:
        return False


CHECKS = [("r38_day_two_exam_confirmed_without_new_study_load", r38_day_two_exam_confirmed_without_new_study_load, 1.25)]
