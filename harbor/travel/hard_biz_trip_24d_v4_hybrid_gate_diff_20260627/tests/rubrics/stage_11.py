"""Stage 11: the client lunch must exist in banking and the durable budget."""
from __future__ import annotations
from loguru import logger
from ._helpers import _any, _agent_used_tool, _agent_used_tool_with_args, _workspace_file_nonempty, _workspace_file_text, _bank_lunch_state


def s11_recorded_expense(env) -> bool:
    text = _workspace_file_text(env, "/workspace/budget.md").lower()
    described = _any(text, ["6800", "jpy"]) and _any(text, ["lunch", "client"])
    ok = described and _workspace_file_nonempty(env, "/workspace/budget.md") and _bank_lunch_state(env)
    logger.info(f"s11_recorded_backend: {ok}"); return ok


def s11_checked_email_banking(env) -> bool:
    has_email = _agent_used_tool(env, "email", "search_emails", stage=11) or _agent_used_tool(env, "email", "read_email", stage=11)
    has_bank = _agent_used_tool_with_args(env, "banking", "list_transactions", ["acct_zhangming_jpy_wallet"], stage=11)
    ok = has_email and has_bank and s11_recorded_expense(env)
    logger.info(f"s11_checked: {ok}"); return ok


CHECKS = [("s11_recorded_expense", s11_recorded_expense, 1.5), ("s11_checked_email_banking", s11_checked_email_banking, 1.5)]
