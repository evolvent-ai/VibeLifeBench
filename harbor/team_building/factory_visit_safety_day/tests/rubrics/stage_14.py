from __future__ import annotations
from ._helpers import *


def s14_option_summary_draft(env) -> bool:
    return used_tool(env, 14, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["confirmation", "option"]],
        recipient_terms=["wei.ran"],
        body_groups=[["factory", "supplier"], ["PPE", "protection"], ["driver", "transport"], ["deposit", "payment"], ["pending", "confirmation"]],
    )


CHECKS = [("s14_option_summary_draft", s14_option_summary_draft, 1.5)]
