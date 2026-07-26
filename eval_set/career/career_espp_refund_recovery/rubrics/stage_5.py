"""Stage 5 — 对正确证券账户、标的、行情与公司方案做完整对账。"""
from __future__ import annotations

from ._helpers import norm_num, position_for, quote_for, record_text, stage_call_matches, text_has

ACCOUNT_ID = "acct_eq_main"
SYMBOL = "689612"
QTY_MILLI = 4_955_000
PRICE_MINOR = 6_000
HISTORY_MESSAGE_ID = "<20240418-espp-plan@ximingsemi.com>"
_BAD_BASE = ("持股计划价差基数按月均工资", "股权价差基数为工资", "按工作年限和工资计算股权", "按工龄计算股权")


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
    corpus = norm_num(record)
    values = (ACCOUNT_ID, SYMBOL, "4955", "60.00", "297300", "200300", "97000", "2026-05-08")
    return all(value.lower() in corpus for value in values) and text_has(record, [["差额"], ["参考公允价值"]])


def s5_contract_valuation_method(env) -> bool:
    if not _objects_ok(env):
        return False
    record = record_text(env, "severance_review.md")
    if any(term in record for term in _BAD_BASE):
        return False
    return HISTORY_MESSAGE_ID.lower() in record and text_has(record, [
        ["原约定"], ["已归属"], ["基准日"], ["收盘价", "市场价"],
        ["4955×60.00=297300", "4955*60.00=297300", "4955×60=297300"],
        ["不是股权价差基数", "工资仅作收入旁证"],
    ])


CHECKS = [
    ("s5_reconcile_diff", s5_reconcile_diff, 3.5),
    ("s5_contract_valuation_method", s5_contract_valuation_method, 3.0),
]
