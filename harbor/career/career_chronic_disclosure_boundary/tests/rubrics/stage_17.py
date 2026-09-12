"""Stage 17 — query company payment and reconcile exactly。"""
from __future__ import annotations

from ._helpers import derived_text, norm_num, severance_deposit_minor, stage_write_used, text_has, trace_result_text, used_tool

_TX_ID = "BKT-20260716-PAY-75lf43k7xtx"


def _backend_trace(env) -> bool:
    trace = trace_result_text(env, 17, "list_transactions")
    return used_tool(env, "list_transactions", stage=17) and _TX_ID.lower() in trace and "20540000" in norm_num(trace)


def s17_severance_paid_backend(env) -> bool:
    return _backend_trace(env) and severance_deposit_minor(env) == 20540000


def s17_paid_amount_reconciled(env) -> bool:
    if not s17_severance_paid_backend(env) or not stage_write_used(env, 17):
        return False
    raw = derived_text(env)
    corpus = norm_num(raw)
    values = all(value in corpus for value in ("205400", "302400", "97000"))
    source = _TX_ID.lower() in raw.lower() and "2026-07-16" in raw
    semantics = text_has(raw, [["credited", "deposited", "paid"], ["lawful"], ["difference", "remaining"], ["outstanding", "due", "remaining"]])
    return values and source and semantics


CHECKS = [
    ("s17_severance_paid_backend", s17_severance_paid_backend, 1.5),
    ("s17_paid_amount_reconciled", s17_paid_amount_reconciled, 3.0),
]
