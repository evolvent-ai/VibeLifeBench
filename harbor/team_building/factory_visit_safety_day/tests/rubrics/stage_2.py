from __future__ import annotations
from ._helpers import *


def s2_finance_draft(env) -> bool:
    drafted = used_tool(env, 2, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["invoice", "budget"]],
        recipient_terms=["finance"],
        body_groups=[["bus", "charter"], ["catering"], ["insurance"], ["budget"], ["invoice"]],
    )
    return drafted and workspace_file_has(env, "BUDGET_LEDGER.csv", [["bus", "charter"], ["lunch", "catering"], ["insurance"], ["invoice"]])


CHECKS = [("s2_finance_draft", s2_finance_draft, 1.5)]
