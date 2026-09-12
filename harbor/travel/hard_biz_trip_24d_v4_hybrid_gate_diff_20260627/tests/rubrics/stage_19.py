"""Stage 19: actual bank reconciliation and durable discrepancy record."""
from __future__ import annotations
from loguru import logger
from ._helpers import _any, _agent_used_tool, _workspace_file_nonempty, _workspace_file_text, _bank_reconciliation_state, _bank_forex_state, _refund_pending_backend


def s19_must_find_discrepancy(env) -> bool:
    text=(_workspace_file_text(env,"/workspace/budget.md")+"\n"+_workspace_file_text(env,"/workspace/evidence_log.md")).lower()
    described=_any(text,["discrepancy","difference","variance","actual payment","reconcile"]) and _any(text,["bank","transaction","statement","charge"]) and _any(text,["mu524","refund","pending","not received"]) and _any(text,["1.5%","ftf","fee","hong kong","hkg","200"])
    ok=described and _bank_reconciliation_state(env) and _bank_forex_state(env) and _refund_pending_backend(env) and s19_tool_and_persist(env)
    logger.info(f"s19_must_backend: {ok}"); return ok


def s19_tool_and_persist(env) -> bool:
    text=_workspace_file_text(env,"/workspace/budget.md").lower()
    used=_agent_used_tool(env,"banking","list_transactions",stage=19) and _agent_used_tool(env,"banking","list_accounts",stage=19)
    described=_any(text,["pending refund","pending","not received"]) and _any(text,["1.5%","ftf","foreign transaction fee"])
    ok=used and _workspace_file_nonempty(env,"/workspace/budget.md") and described and _bank_reconciliation_state(env)
    logger.info(f"s19_tool_backend: {ok}"); return ok


CHECKS=[("s19_must_find_discrepancy",s19_must_find_discrepancy,3.0),("s19_tool_and_persist",s19_tool_and_persist,1.5)]
