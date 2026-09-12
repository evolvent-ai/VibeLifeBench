from __future__ import annotations
from ._helpers import *


def s9_shortlist_draft(env) -> bool:
    return used_tool(env, 9, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["primary", "candidate"]],
        recipient_terms=["wei.ran"],
        body_groups=[["primary", "main"], ["backup"], ["budget"], ["pending"]],
    )


CHECKS = [("s9_shortlist_draft", s9_shortlist_draft, 1.5)]
