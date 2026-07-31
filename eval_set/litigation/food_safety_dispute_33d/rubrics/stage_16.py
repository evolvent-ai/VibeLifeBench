"""Stage 16: 判决送达(world, 判退一赔十) — 响应结果, 预警15日上诉期."""
from __future__ import annotations

from ._helpers import _stage_corpus
from .cross_stage import d_appeal_window_15d


def s16_responds_judgment(env) -> bool:
    """响应判决结果(退一赔十+就医损失)。"""
    text = _stage_corpus(env, 16)
    has_result = any(k in text for k in ["判决", "胜诉", "支持", "退一赔十", "十倍赔偿"])
    has_medical = any(k in text for k in ["医疗费", "就医费", "320"])
    has_next = any(k in text for k in ["上诉期", "十五日", "15日", "执行", "申请执行", "由你决定"])
    return has_result and has_medical and has_next


CHECKS = [
    ("d_appeal_window_15d", d_appeal_window_15d, 0.5),
]
