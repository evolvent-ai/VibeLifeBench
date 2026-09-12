from __future__ import annotations
from ._helpers import *


def s1_email_read_goal(env) -> bool:
    return (
        (
            used_tool_with_value(env, 1, "email", "search_emails", ["cross-cultural icebreaking", "onboarding new colleagues", "low-intensity inclusion", "organizational belonging"])
            or used_tool_with_value(env, 1, "email", "get_emails", ["cross-cultural icebreaking", "onboarding new colleagues", "low-intensity inclusion", "organizational belonging"])
        )
        and workspace_has(env, "CITY_CULTURE_PLAN.json", ["cross-cultural icebreaking", "onboarding new colleagues", "low-intensity inclusion", "organizational belonging"], 3, stage=1)
    )


CHECKS = [("s1_email_read_goal", s1_email_read_goal, 1.25)]
