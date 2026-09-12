from __future__ import annotations
from ._helpers import *


def s21_forklift_update(env) -> bool:
    return (
        notification_from_trace(env, 21, ["stairway construction", "photo stop", "group reminders", "accessible detour"])
        and used_tool(env, 21, "notion", "API-patch-block-children")
        and workspace_has(env, "POST_EVENT_REVIEW.md", ["stairway construction", "photo stop", "group reminders", "accessible detour"], 4, stage=21)
    )


CHECKS = [("s21_forklift_update", s21_forklift_update, 1.5)]
