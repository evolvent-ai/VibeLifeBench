"""Stage 19: 二审期限与审理范围 — 日历和 Notion 双持久化。"""
from __future__ import annotations

from ._helpers import _assistant_calendar_text, _food_journal_text


def s19_appeal_deadlines_calendar(env) -> bool:
    text = _assistant_calendar_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_second = any(key in text for key in ("二审", "被上诉", "上诉"))
    has_response = any(key in text for key in ("答辩", "应诉", "举证"))
    has_deadline = any(key in text for key in ("期限", "截止", "15日", "十五日", "2026-07"))
    return has_second and has_response and has_deadline


def s19_second_instance_diff(env) -> bool:
    text = _food_journal_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_scope = any(key in text for key in ("围绕上诉请求", "上诉请求范围", "二审审理范围"))
    has_evidence = any(key in text for key in ("检验报告", "证据目录", "补充证据", "一审证据"))
    has_cost = any(key in text for key in ("诉讼费", "费用", "预交"))
    return has_scope and has_evidence and has_cost


CHECKS = [
    ("s19_assistant_appeal_deadlines_calendar", s19_appeal_deadlines_calendar, 0.5),
    ("s19_persisted_second_instance_plan", s19_second_instance_diff, 0.5),
]
