from __future__ import annotations
from ._helpers import *


def s14_option_summary_draft(env) -> bool:
    return used_tool(env, 14, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["确认选项", "决策选项"]],
        recipient_terms=["wei.ran"],
        body_groups=[["工厂", "供应商"], ["ppe", "防护"], ["司机", "交通"], ["押金", "付款"], ["待确认"]],
    )


CHECKS = [("s14_option_summary_draft", s14_option_summary_draft, 1.5)]
