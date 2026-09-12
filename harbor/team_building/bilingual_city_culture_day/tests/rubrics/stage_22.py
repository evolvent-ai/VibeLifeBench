from __future__ import annotations
from ._helpers import *


def s22_late_need_discovered(env) -> bool:
    return (
        notification_from_trace(env, 22, ["insufficient noise reminders", "English safety reminder"])
        and workspace_has(env, "POST_EVENT_REVIEW.md", ["insufficient noise reminders", "English safety reminder", "late report", "improvement"], 4, stage=22)
    )


CHECKS = [("s22_late_need_discovered", s22_late_need_discovered, 1.75)]
