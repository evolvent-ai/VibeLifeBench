"""Stage 17 — 绑定工资卡、唯一交易、付款方、余额和完整差额对账。"""
from __future__ import annotations

from ._helpers import account_by_id, norm_num, record_text, stage_call_matches, text_has, transaction_by_id

AMOUNT_MINOR = 20_030_000
EMPLOYER = "矽鸣半导体技术(上海)有限公司"


def _payment_object(env) -> dict | None:
    if not stage_call_matches(env, 17, "list_transactions", {"account_id": "acct_gk_checking"}):
        return None
    tx = transaction_by_id(env, "tx_gk_severance", "acct_gk_checking")
    account = account_by_id(env, "acct_gk_checking")
    if not tx or not account:
        return None
    if int(tx.get("amount_minor") or 0) != AMOUNT_MINOR or str(tx.get("kind") or "") != "deposit":
        return None
    if str(tx.get("counterparty") or "") != EMPLOYER or "持股计划赎回款" not in str(tx.get("memo") or ""):
        return None
    if str(tx.get("posted_at") or "") != "2026-07-16T08:00:00Z":
        return None
    if int(tx.get("balance_after_minor") or -1) != int(account.get("balance_minor") or -2):
        return None
    return tx


def s17_equity_payment_backend(env) -> bool:
    tx = _payment_object(env)
    if not tx:
        return False
    record = record_text(env, "severance_review.md")
    required = ("acct_gk_checking", "tx_gk_severance", EMPLOYER.lower(), str(tx.get("posted_at") or ""), str(tx.get("balance_after_minor") or ""))
    return all(value.lower() in record for value in required) and "200300" in norm_num(record)


def s17_payment_reconciled(env) -> bool:
    if not _payment_object(env):
        return False
    record = record_text(env, "severance_review.md")
    corpus = norm_num(record)
    if not all(value in corpus for value in ("tx_gk_severance", "200300", "297300", "97000")):
        return False
    if any(term in record for term in ("确认全额结清", "视为全部支付", "差额已结清")):
        return False
    return text_has(record, [
        ["部分支付", "部分款项", "部分受领"],
        ["保留继续主张", "保留主张", "不视为全额结清"],
        ["未补差额", "差额97000", "差额 97000"],
    ])


CHECKS = [
    ("s17_equity_payment_backend", s17_equity_payment_backend, 2.0),
    ("s17_payment_reconciled", s17_payment_reconciled, 3.5),
]
