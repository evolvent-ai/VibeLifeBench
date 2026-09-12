"""Stage 17: departure and interim reconciliation, without requiring future Stage-19 forex facts."""
from __future__ import annotations
from loguru import logger
from ._helpers import _any, _stage_corpus, _agent_used_tool, _workspace_file_nonempty, _text_has_backend_flight_amounts, _text_has_backend_hotel_amounts, _bank_lunch_state, _refund_pending_backend


def s17_expense_tracking(env) -> bool:
    text=_stage_corpus(env,17)
    has_bank=_agent_used_tool(env,"banking","list_transactions",stage=17) or _agent_used_tool(env,"banking","list_accounts",stage=17)
    tracking=_any(text,["budget","actual","variance","refund","pending","expense"])
    pending=_any(text,["mu524","refund","pending","not received","pending refund"])
    amounts=_text_has_backend_flight_amounts(env,text) and _text_has_backend_hotel_amounts(env,text)
    persisted=_workspace_file_nonempty(env,"/workspace/budget.md")
    ok=has_bank and persisted and tracking and pending and amounts and _bank_lunch_state(env) and _refund_pending_backend(env)
    logger.info(f"s17_expense_backend: {ok}"); return ok


CHECKS=[("s17_expense_tracking",s17_expense_tracking,2.0)]
