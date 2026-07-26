"""Stage 21: 复盘总结 — Notion 总结 + 经验教训 + 二审阶段方向(side effect+text)."""
from __future__ import annotations

from ._helpers import _notion_page_text, _stage_corpus


def s21_retro_in_notion(env) -> bool:
    """复盘总结写进 Notion (过程/节点/证据法条/成本)。"""
    text = _notion_page_text(env, "复盘") or _notion_page_text(env, "总结") or _notion_page_text(env, "民间借贷追偿")
    if text is None:
        return False  # required evidence unavailable → fail closed
    n = sum(1 for k in ["复盘", "总结", "经验", "教训", "证据", "法条", "本金", "节点"] if k in text)
    return n >= 2


def s21_lessons_learned(env) -> bool:
    """记录借贷经验教训 (砍头息/现金留凭证/担保写清/及时催收)。"""
    text = _stage_corpus(env, 21)
    return any(k in text for k in ["砍头息", "现金", "留凭证", "留证", "担保", "催收", "及时", "教训", "经验"])


def s21_next_steps(env) -> bool:
    """给出二审阶段的准备方向。"""
    text = _stage_corpus(env, 21)
    has_appeal = any(k in text for k in ["二审", "上诉", "应诉", "庭审", "答辩"])
    has_direction = any(k in text for k in ["准备", "方向", "证据", "下一步", "建议"])
    return has_appeal and has_direction


CHECKS = [
    ("s21_retro_in_notion", s21_retro_in_notion, 0.5),
    ("s21_lessons_learned", s21_lessons_learned, 0.5),
    ("s21_next_steps", s21_next_steps, 0.5),
]
