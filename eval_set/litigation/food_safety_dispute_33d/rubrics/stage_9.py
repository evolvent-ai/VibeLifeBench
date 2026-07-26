"""Stage 9: 程序期限进日历 + 申请食品检验(标签/非法添加认定的关键)."""
from __future__ import annotations

from ._helpers import _stage_corpus, _all_events_text
from .cross_stage import d_import_chinese_label, d_limitation_three_years


def s9_deadlines_in_calendar(env) -> bool:
    """关键程序期限(举证/检验/开庭/上诉期)进日历。"""
    text = _all_events_text(env)
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["举证", "检验", "开庭", "上诉", "答辩", "期限", "立案"])


def s9_apply_inspection(env) -> bool:
    """说明申请食品检验的程序与重要性(过错/标签/非法添加认定)。"""
    text = _stage_corpus(env, 9)
    return any(k in text for k in ["检验", "申请检验", "送检", "CMA", "非法添加", "标签符合性"])


CHECKS = [
    ("d_import_chinese_label", d_import_chinese_label, 1),
    ("d_limitation_three_years", d_limitation_three_years, 0.5),
]
