from __future__ import annotations
from ._helpers import *


def s2_finance_draft(env) -> bool:
    return (
        used_tool(env, 2, "email", "save_draft")
        and draft_matches(env, "invoice", "finance", ["guided tour", "catering", "transportation", "itemized", "deposit", "confirmation"], stage=2)
        and workspace_has(env, "BUDGET_LEDGER.csv", ["46000", "guide", "dim_sum", "transport", "invoice", "pending"], 4, stage=2)
    )


CHECKS = [("s2_finance_draft", s2_finance_draft, 1.5)]
