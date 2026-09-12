"""Stage 17: verify and reconcile the severance deposit."""
from __future__ import annotations
from ._helpers import derived_text, norm_num, severance_deposit_minor, text_has, used_tool

_TX_ID = "BKT-20260716-PAY-tvzlvguqcvx"


def s17_severance_paid_backend(env) -> bool:
    return used_tool(env, "list_transactions", stage=17, server="banking") and severance_deposit_minor(env) == 20450000


def s17_paid_amount_reconciled(env) -> bool:
    if not s17_severance_paid_backend(env):
        return False
    raw = derived_text(env)
    compact = norm_num(raw)
    return _TX_ID.lower() in raw.lower() and all(value in compact for value in ("204500", "301500", "97000")) and text_has(raw, [["shortfall", "gap", "below", "underpaid", "insufficient"], ["shortfall", "shortfall", "back payment", "still due"]])


CHECKS = [("s17_severance_paid_backend", s17_severance_paid_backend, 1.5), ("s17_paid_amount_reconciled", s17_paid_amount_reconciled, 3.0)]
