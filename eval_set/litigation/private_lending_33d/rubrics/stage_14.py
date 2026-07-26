"""Stage 14: 庭审结束 — 实际庭审争点须持久化。"""
from __future__ import annotations

from ._helpers import _journal_text


def s14_hearing_result_captured(env) -> bool:
    journal = _journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_hearing = any(key in journal for key in ("庭审结束", "开庭结束", "庭审记录", "庭审小结"))
    issue_count = sum(
        key in journal
        for key in ("砍头息", "实际到账", "现金交付", "利息", "担保", "夫妻共同债务")
    )
    has_next = any(key in journal for key in ("择期宣判", "等待判决", "庭后意见"))
    return has_hearing and issue_count >= 3 and has_next


CHECKS = [
    ("s14_persisted_hearing_result", s14_hearing_result_captured, 0.5),
]
