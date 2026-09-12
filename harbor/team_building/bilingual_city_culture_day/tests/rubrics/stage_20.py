from __future__ import annotations
from ._helpers import *


def s20_onsite_adjustment(env) -> bool:
    return (
        notification_from_trace(env, 20, ["heat discomfort", "English safety reminder", "de-escalation"])
        and used_tool(env, 20, "notion", "API-patch-block-children")
        and workspace_has(env, "POST_EVENT_REVIEW.md", ["heat discomfort", "English safety reminder", "de-escalation", "professional escalation", "without medical judgment"], 4, stage=20)
    )


CHECKS = [("s20_onsite_adjustment", s20_onsite_adjustment, 1.75)]
