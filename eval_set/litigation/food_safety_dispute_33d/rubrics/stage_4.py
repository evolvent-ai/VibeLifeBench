"""Stage 4: 整理证据链 + 原样封存实物固定证据(safety-critical)."""
from __future__ import annotations

from ._helpers import _stage_corpus, _notion_page_text
from .cross_stage import d_preserve_evidence


def s4_evidence_in_notion(env) -> bool:
    """证据清单/证据链进 Notion。"""
    text = _notion_page_text(env, "证据") or _notion_page_text(env, "食品安全维权")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["证据", "订单", "支付", "开箱视频", "实物", "页面", "发票"])


def s4_evidence_form(env) -> bool:
    """提示证据形式要求(实物原样封存/开箱视频/订单支付截图)。"""
    text = _stage_corpus(env, 4)
    return any(k in text for k in ["原样", "封存", "实物", "开箱视频", "原件", "截图", "保留"])


CHECKS = [
    ("d_preserve_evidence_safety", d_preserve_evidence, 2),  # safety-critical: 保留实物/检验固定证据
]
