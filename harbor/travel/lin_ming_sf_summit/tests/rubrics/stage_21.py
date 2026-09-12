"""Stage 21 checker: notification — reimbursement policy update."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _stage_tools,
    _tool_called_in_stage,
    _tool_with_args,
    _notion_text,
    _any,
    _trace_successful,
)


def s21_reimbursement_synced(env) -> bool:
    """Stage 21 called get_reimbursement_remaining, list_approvals, or read reimbursement policy AND called notion create_page / update_page / append_block_children AND _notion_text contains flight/hotel/expense info."""
    ok_policy = False
    tools = _stage_tools(env, 21)
    for tc in tools:
        if not _trace_successful(tc):
            continue
        name = (tc.get("name") or "").lower()
        if any(k in name for k in [
            # Real banking tools read the reimbursement/approval state via account + ledger
            # (get_reimbursement_remaining / list_approvals were phantom tools).
            "get_account",
            "list_accounts",
            "list_transactions",
            "reimbursement",
            "policy",
        ]):
            ok_policy = True
            break
    if not ok_policy:
        for tc in tools:
            if not _trace_successful(tc):
                continue
            name = (tc.get("name") or "").lower()
            if "read" in name:
                args = str(tc.get("arguments") or {})
                if _any(args, ["reimbursement", "reimbursement", "policy", "policy", "expense standard", "travel"]):
                    ok_policy = True
                    break

    # Real notion tool names are API-post-page / API-patch-page / API-patch-block-children.
    # _tool_called_in_stage does a lowercased substring match, so match the serialized forms.
    notion_tool = _tool_called_in_stage(env, 21, ["post-page", "post_page", "patch-page", "patch_page", "patch-block-children", "patch_block_children"])
    text = _notion_text(env)
    has_expense_info = _any(text, ["flight", "hotel", "expense", "expense", "flight", "hotel", "reimbursement", "travel", "budget"])
    ok = ok_policy and notion_tool and has_expense_info
    logger.info(f"s21_reimbursement_synced: policy={ok_policy} notion={notion_tool} expense_info={has_expense_info} -> {ok}")
    return ok


CHECKS = [
    ("s21_reimbursement_synced", s21_reimbursement_synced, 1.5),
]
