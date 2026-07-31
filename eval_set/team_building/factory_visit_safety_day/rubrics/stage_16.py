from __future__ import annotations
from ._helpers import *


def s16_approver_reply(env) -> bool:
    return used_tool(env, 16, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["安全边界", "评审回复"]],
        recipient_terms=["approver"],
        body_groups=[["业务理解"], ["安全"], ["自愿", "退出"], ["补充", "修订"]],
    )


CHECKS = [("s16_approver_reply", s16_approver_reply, 1.0)]
