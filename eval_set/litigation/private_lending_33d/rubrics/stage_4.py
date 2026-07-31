"""Stage 4: 证据链整理 — 大额现金交付举证风险 + 证据清单进 Notion."""
from __future__ import annotations

from ._helpers import _stage_corpus, _notion_page_text
from .cross_stage import d_cash_delivery_risk


def s4_evidence_list_in_notion(env) -> bool:
    """证据清单写进 Notion (side effect)。"""
    text = _notion_page_text(env, "证据") or _notion_page_text(env, "民间借贷追偿")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["证据", "借条", "转账", "微信", "催收"])


def s4_evidence_inventory(env) -> bool:
    """列出了多类关键证据 (借条/转账回单/微信催收/还款记录/证人)。"""
    text = _stage_corpus(env, 4)
    n = sum(1 for k in ["借条", "转账", "回单", "微信", "催收", "还款", "证人", "林涛"] if k in text)
    return n >= 3


CHECKS = [
    ("s4_evidence_list_in_notion", s4_evidence_list_in_notion, 0.5),
    ("s4_evidence_inventory", s4_evidence_inventory, 0.5),
    ("d_cash_delivery_risk", d_cash_delivery_risk, 1),
]
