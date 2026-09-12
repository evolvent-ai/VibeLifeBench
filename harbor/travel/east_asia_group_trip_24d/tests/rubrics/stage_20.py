"""Stage 20: machine-readable per-person settlement, refund state, 4/3 split and cap."""
from __future__ import annotations

import re
from loguru import logger

from ._helpers import _agent_used_any_tool, _workspace_file_text

_USERS=("usr_chen_yu","usr_li_ting","usr_wang_hao","usr_zhao_min")
_CAP=540_000


def _settlement(budget: str) -> tuple[dict[str,int], int | None]:
    totals={}
    for user in _USERS:
        m=re.search(rf"user_id\s*=\s*{re.escape(user)}\s*;[^\n]*settled_total_minor\s*=\s*(\d+)",budget)
        if m: totals[user]=int(m.group(1))
    z=re.search(r"user_id\s*=\s*usr_zhao_min\s*;[^\n]*seoul_minor\s*=\s*(\d+)",budget)
    return totals,int(z.group(1)) if z else None


def s20_gate(env) -> bool:
    used_banking=_agent_used_any_tool(env,[("banking","list_transactions"),("banking","get_account"),("banking","list_accounts")],stage=20)
    budget=_workspace_file_text(env,"/workspace/budget.md").casefold()
    totals,zhao_seoul=_settlement(budget)
    header=all(x in budget for x in ("status=settled","cap_minor=540000","tokyo_split_count=4","seoul_split_count=3"))
    refund=any(x in budget for x in ("pending refund","refund_status="))
    exact= set(totals)==set(_USERS) and all(0<=v<=_CAP for v in totals.values()) and zhao_seoul==0
    ok=bool(used_banking and header and refund and exact)
    logger.info("s20_gate: banking={} header={} refund={} totals={} zhao={} -> {}",used_banking,header,refund,totals,zhao_seoul,"PASS" if ok else "FAIL")
    return ok


def s20b_gate(env) -> bool:
    budget=_workspace_file_text(env,"/workspace/budget.md").casefold()
    totals,zhao_seoul=_settlement(budget)
    # The ledger must distinguish refund amount/status/owner rather than merely mention the word.
    refund_line=any(
        "refund" in line
        for line in budget.splitlines()
        if any(token in line for token in ("amount_minor=","refund_minor=")) and any(token in line for token in ("status=","owner="))
    )
    return bool(set(totals)==set(_USERS) and zhao_seoul==0 and refund_line and len(set(totals.values()))>=2)


CHECKS=[("s20_gate",s20_gate,2.5),("s20b_gate",s20b_gate,1.5)]
