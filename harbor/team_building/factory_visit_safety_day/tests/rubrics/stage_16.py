from __future__ import annotations
from ._helpers import *


def s16_approver_reply(env) -> bool:
    return used_tool(env, 16, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["safety", "review"]],
        recipient_terms=["approver"],
        body_groups=[["business-understanding"], ["safety"], ["voluntary", "exit"], ["add", "update"]],
    )


CHECKS = [("s16_approver_reply", s16_approver_reply, 1.0)]
