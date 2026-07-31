from __future__ import annotations
from ._helpers import *


def s9_shortlist_draft(env) -> bool:
    return used_tool(env, 9, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["主备方案", "候选方案"]],
        recipient_terms=["wei.ran"],
        body_groups=[["主方案", "首选"], ["备选"], ["预算"], ["待确认"]],
    )


CHECKS = [("s9_shortlist_draft", s9_shortlist_draft, 1.5)]
