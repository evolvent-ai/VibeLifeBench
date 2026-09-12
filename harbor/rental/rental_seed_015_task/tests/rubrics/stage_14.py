from __future__ import annotations
from ._helpers import *


def s14_early_release_calendar_rechecked(env) -> bool:
    return (
        tool_stage(env, 14, CALENDAR, None, [])
        and tool_stage(env, 14, NOTICE, None, ["ntf_school_early_release"])
        and _has_parts(calendar_event("evt_school_early_release", env), ["early dismissal", "16:35", "17:20", "2026-08-07"])
        and notification_has(env, "ntf_school_early_release", ["heat", "aftercare"])
        and stage_notion_any(env, 14, (["early dismissal", "pickup"], ["16:35", "aftercare"]))
        and notion_has_any(env, (["early dismissal", "16:35", "17:20"], ["school calendar", "pickup recovery"]))
    )


CHECKS = [("s14_early_release_calendar_rechecked", s14_early_release_calendar_rechecked, 1.75)]
