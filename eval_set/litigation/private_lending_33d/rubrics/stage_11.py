"""Stage 11: 质证应对 — 接受砍头息(本金按实际36万) + 现金交付举证应对; 落 Notion."""
from __future__ import annotations

from ._helpers import _stage_corpus, _notion_page_text
from .cross_stage import d_defense_kantou_accepted


def s11_finds_supporting_case(env) -> bool:
    """检索到支持质证的同类判例 (case_001 砍头息本金按实际 / case_012 现金交付正面认定)。"""
    text = _stage_corpus(env, 11)
    return any(k in text for k in ["case_001", "case_012", "case_003", "本金按实际", "现金交付", "取现凭证", "综合认定"])


def s11_rebuttal_in_notion(env) -> bool:
    """质证意见落到 Notion (side effect)。"""
    text = _notion_page_text(env, "质证") or _notion_page_text(env, "民间借贷追偿")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["质证", "反驳", "本金", "砍头息", "现金", "交付"])


CHECKS = [
    ("s11_finds_supporting_case", s11_finds_supporting_case, 0.5),
    ("s11_rebuttal_in_notion", s11_rebuttal_in_notion, 0.5),
    ("d_defense_kantou_accepted", d_defense_kantou_accepted, 0.5),
]
