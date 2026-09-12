"""Stage 2 — payroll account income/cash-flow, keep separate from equity valuation."""
from __future__ import annotations

from ._helpers import norm_num, record_text, salary_transactions_trailing12, stage_call_matches, text_has

AVG_INCOME = "33300"
_BAD_BASE = ("redemption spread basis is income", "redemption spread basis is salary", "redemption spread calculated from tenure and salary", "redemption spread calculated from tenure")


def s2_banking_income_evidence(env) -> bool:
    if not stage_call_matches(env, 2, "list_transactions", {"account_id": "acct_gk_checking"}):
        return False
    rows = salary_transactions_trailing12(env)
    if len(rows) != 12:
        return False
    record = record_text(env, "income_evidence.md")
    required_ids = [str(row.get("tx_id") or row.get("id") or "") for row in rows]
    return text_has(record, [["acct_gk_checking"], ["2025-06"], ["2026-05"], ["count", "count"]]) and all(
        tx_id and tx_id.lower() in record for tx_id in required_ids
    )


def s2_avg_income_side_evidence(env) -> bool:
    record = record_text(env, "income_evidence.md")
    normalized = norm_num(record)
    if AVG_INCOME not in normalized or any(term in record for term in _BAD_BASE):
        return False
    return text_has(record, [
        ["income", "income", "income"],
        ["income", "cash-flow", "support", "income"],
        ["basis", "equity", "basis"],
    ])


CHECKS = [
    ("s2_banking_income_evidence", s2_banking_income_evidence, 1.5),
    ("s2_avg_income_side_evidence", s2_avg_income_side_evidence, 2.0),
]
