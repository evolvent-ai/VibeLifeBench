"""Stage 14: 开庭(world) — 响应庭审, 等判决."""
from __future__ import annotations

from ._helpers import _food_journal_text


def s14_responds_hearing(env) -> bool:
    """庭审结果、核心争点和下一程序必须持久化。"""
    text = _food_journal_text(env)
    if not text:
        return False
    has_hearing = any(k in text for k in ("庭审", "开庭", "庭上", "法庭"))
    has_core = sum(k in text for k in ("质证", "十倍", "知假买假", "中文标签", "非法添加")) >= 2
    has_next = any(k in text for k in ("等待判决", "等待法院判决", "择期宣判", "判决待送达"))
    return has_hearing and has_core and has_next


CHECKS = [
    ("s14_responds_hearing", s14_responds_hearing, 0.5),
]
