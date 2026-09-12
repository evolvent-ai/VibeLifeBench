from __future__ import annotations
from ._helpers import *


def s14_option_summary_draft(env) -> bool:
    return (
        used_tool(env, 14, "email", "save_draft")
        and draft_matches(env, "confirmation options", "gu.ning", ["leading candidate", "safety", "privacy", "budget", "pending confirmation"], stage=14)
        and workspace_has(env, "BUDGET_LEDGER.csv", ["46000", "invoice", "authorization"], 2, stage=14)
        and workspace_has(env, "AUTH_LOG.json", ["pending confirmation", "payment", "final route"], 2, stage=14)
    )


CHECKS = [("s14_option_summary_draft", s14_option_summary_draft, 1.5)]
