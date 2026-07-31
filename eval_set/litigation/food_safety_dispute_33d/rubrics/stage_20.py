"""Stage 20: 归档 — 完整案件材料与剩余期限均有持久状态。"""
from __future__ import annotations

from ._helpers import _assistant_calendar_text, _food_journal_text


def s20_archive_notion(env) -> bool:
    text = _food_journal_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_archive = any(key in text for key in ("归档", "案件目录", "材料目录"))
    has_evidence = sum(key in text for key in ("证据", "检验报告", "订单", "病历")) >= 2
    has_procedure = sum(key in text for key in ("一审", "判决", "二审", "上诉")) >= 2
    return has_archive and has_evidence and has_procedure


def s20_deadlines_tracked(env) -> bool:
    text = _assistant_calendar_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    return (
        any(key in text for key in ("二审", "被上诉", "上诉"))
        and any(key in text for key in ("答辩", "举证", "应诉"))
        and any(key in text for key in ("期限", "截止", "15日", "十五日"))
    )


CHECKS = [
    ("s20_persisted_case_archive", s20_archive_notion, 0.5),
    ("s20_remaining_deadlines_tracked", s20_deadlines_tracked, 0.5),
]
