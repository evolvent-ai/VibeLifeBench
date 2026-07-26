from __future__ import annotations
from ._helpers import *


def s2_finance_draft(env) -> bool:
    drafted = used_tool(env, 2, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["发票", "预算"]],
        recipient_terms=["finance"],
        body_groups=[["包车"], ["餐饮"], ["保险"], ["预算"], ["发票"]],
    )
    return drafted and workspace_file_has(env, "BUDGET_LEDGER.csv", [["bus", "包车"], ["lunch", "餐饮"], ["insurance", "保险"], ["invoice", "发票"]])


CHECKS = [("s2_finance_draft", s2_finance_draft, 1.5)]
