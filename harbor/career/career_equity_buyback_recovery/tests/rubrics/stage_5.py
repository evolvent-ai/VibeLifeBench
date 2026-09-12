"""Stage 5 — reconcile the correct securities account, security, quote, and company proposal."""
from __future__ import annotations

from ._helpers import has_values, position_for, quote_for, record_text, stage_call_matches, text_has

ACCOUNT_ID = "acct_eq_main"
SYMBOL = "689611"
QTY_MILLI = 5_000_000
PRICE_MINOR = 5_942
HISTORY_MESSAGE_ID = "<20240520-rsu-plan@yiweicloud.com>"
_BAD_BASE = ("equity buyback shortfall basis is average monthly income", "equity price-difference basis is salary", "equity calculated from tenure and salary", "equity calculated from tenure")


def _objects_ok(env) -> bool:
    if not stage_call_matches(env, 5, "get_positions", {"account_id": ACCOUNT_ID}):
        return False
    if not stage_call_matches(env, 5, "get_quote", {"symbol": SYMBOL}):
        return False
    position = position_for(env, ACCOUNT_ID, SYMBOL)
    quote = quote_for(env, SYMBOL)
    return bool(position and int(position.get("qty_milli") or 0) == QTY_MILLI and quote and int(quote.get("close_minor") or 0) == PRICE_MINOR and str(quote.get("date") or "") == "2026-05-08")


def s5_reconcile_diff(env) -> bool:
    if not _objects_ok(env):
        return False
    record = record_text(env, "severance_review.md")
    values = (ACCOUNT_ID, SYMBOL, "5000", "59.42", "297100", "200100", "97000", "2026-05-08")
    return has_values(record, *values) and text_has(record, [["shortfall"], ["reference"]])


def s5_contract_valuation_method(env) -> bool:
    if not _objects_ok(env):
        return False
    record = record_text(env, "severance_review.md")
    if any(term in record for term in _BAD_BASE):
        return False
    return HISTORY_MESSAGE_ID.lower() in record and text_has(record, [
        ["original"], ["vested"], ["base date"], ["closing", "market"],
        ["5000×59.42=297100", "5000*59.42=297100"],
        ["salary appears here only as income support", "salary is only income support", "salary only as income support"],
    ])


CHECKS = [
    ("s5_reconcile_diff", s5_reconcile_diff, 3.5),
    ("s5_contract_valuation_method", s5_contract_valuation_method, 3.0),
]
