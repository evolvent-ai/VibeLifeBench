"""Stage 2 — 工资卡收入/现金流旁证，不混入持股估值。"""
from __future__ import annotations

from ._helpers import norm_num, record_text, salary_transactions_trailing12, stage_call_matches, text_has

AVG_INCOME = "33300"
_BAD_BASE = ("持股计划价差基数按月均工资", "股权价差基数为工资", "按工作年限和工资计算股权", "按工龄计算股权")


def s2_banking_income_evidence(env) -> bool:
    if not stage_call_matches(env, 2, "list_transactions", {"account_id": "acct_gk_checking"}):
        return False
    rows = salary_transactions_trailing12(env)
    if len(rows) != 12:
        return False
    record = record_text(env, "income_evidence.md")
    required_ids = [str(row.get("tx_id") or row.get("id") or "") for row in rows]
    return text_has(record, [["acct_gk_checking"], ["2025-06"], ["2026-05"], ["样本数12", "样本数 12"]]) and all(
        tx_id and tx_id.lower() in record for tx_id in required_ids
    )


def s2_avg_income_side_evidence(env) -> bool:
    record = record_text(env, "income_evidence.md")
    normalized = norm_num(record)
    if AVG_INCOME not in normalized or any(term in record for term in _BAD_BASE):
        return False
    return text_has(record, [
        ["月均收入", "平均收入", "近12个月"],
        ["收入旁证", "现金流旁证", "仅作旁证", "只作旁证"],
        ["不是股权价差基数", "不作为股权", "不是股权"],
    ])


CHECKS = [
    ("s2_banking_income_evidence", s2_banking_income_evidence, 1.5),
    ("s2_avg_income_side_evidence", s2_avg_income_side_evidence, 2.0),
]
