"""Stage 3 checker — budget / approval policy notification."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _tool_called_in_stage,
    _ws,
    _contains_all,
)


def s3_budget_rules_recorded(env) -> bool:
    """Stage 3 called get_account_balance / get_reimbursement_remaining / list_approvals AND budget_tracker.md contains '15000' and '5000'."""
    ok_tools = _tool_called_in_stage(
        env,
        3,
        [
            # Real banking tools (get_account_balance/get_reimbursement_remaining/list_approvals were phantom).
            "get_account",
            "list_accounts",
            "list_transactions",
        ],
    )
    bt = _ws(env, "/workspace/budget_tracker.md")
    ok_text = _contains_all(bt, ["15000", "5000"])
    ok = ok_tools and ok_text
    logger.info(f"s3_budget_rules_recorded: tools={ok_tools} text={ok_text} -> {ok}")
    return ok


CHECKS = [
    ("s3_budget_rules_recorded", s3_budget_rules_recorded, 1.25),
]
