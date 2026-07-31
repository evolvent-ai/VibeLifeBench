"""Stage 16: 判决送达(world) — 响应判决结果、预警15日上诉期(s_)."""
from __future__ import annotations

from ._helpers import _stage_corpus


def s16_acknowledges_judgment(env) -> bool:
    """对判决结果(支持本金360000, 驳回第二笔/配偶/担保)作出响应。"""
    text = _stage_corpus(env, 16)
    has_amount = any(k in text for k in ["360000", "360,000", "36万", "三十六万"])
    has_result = any(k in text for k in ["判决", "支持", "返还", "驳回", "胜"])
    return has_amount and has_result


CHECKS = [
    ("s16_acknowledges_judgment", s16_acknowledges_judgment, 0.5),
]
