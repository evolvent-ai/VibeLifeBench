"""Stage 17 — bind payroll account, unique transaction, payer, balance, and complete shortfall reconciliation."""
from __future__ import annotations

from ._helpers import account_by_id, has_values, record_text, stage_call_matches, text_has, transaction_by_id

AMOUNT_MINOR = 20_010_000
EMPLOYER = "Yiwei Data Technology (Shanghai) Co., Ltd."


def _payment_object(env) -> dict | None:
    if not stage_call_matches(env, 17, "list_transactions", {"account_id": "acct_gk_checking"}):
        return None
    tx = transaction_by_id(env, "tx_gk_severance", "acct_gk_checking")
    account = account_by_id(env, "acct_gk_checking")
    if not tx or not account:
        return None
    if int(tx.get("amount_minor") or 0) != AMOUNT_MINOR or str(tx.get("kind") or "") != "deposit":
        return None
    if str(tx.get("counterparty") or "") != EMPLOYER or "equity buyback payment" not in str(tx.get("memo") or "").lower():
        return None
    if str(tx.get("posted_at") or "") != "2026-07-16T00:00:00Z":
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
    return all(value.lower() in record for value in required) and has_values(record, "200100")


def s17_payment_reconciled(env) -> bool:
    if not _payment_object(env):
        return False
    record = record_text(env, "severance_review.md")
    if not has_values(record, "tx_gk_severance", "200100", "297100", "97000"):
        return False
    if any(term in record for term in ("confirm fully settled", "treated as fully paid", "shortfall settled")):
        return False
    return text_has(record, [
        ["partial payment", "partial amount", "partial receipt"],
        ["retain the right to continue claiming", "retain the claim", "not treated as fully settled"],
        ["unpaid shortfall", "shortfall 97000"],
    ])


CHECKS = [
    ("s17_equity_payment_backend", s17_equity_payment_backend, 2.0),
    ("s17_payment_reconciled", s17_payment_reconciled, 3.5),
]
