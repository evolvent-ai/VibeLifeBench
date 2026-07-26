"""Stage 23 — benchmark 未来业务阶段的独立深度审计，不控制其他 check。"""
from __future__ import annotations

import re

from ._helpers import list_transactions, record_text


def s23_deep_audit_0(env) -> bool:
    record = record_text(env, "audit_journal.md")
    ids = set(re.findall(r"tx_gk_[0-9a-z]{3,}", record))
    backend = {
        str(row.get("tx_id") or row.get("id") or "")
        for row in list_transactions(env, account_id="acct_gk_checking")
    }
    return "tx_gk_severance" in ids and len(ids) >= 6 and ids.issubset(backend)


CHECKS = [("s23_deep_audit_0", s23_deep_audit_0, 1.5)]
