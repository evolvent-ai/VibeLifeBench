"""Stage 19: 二审应诉期限 — 日历与 Notion 双持久化。"""
from __future__ import annotations

from ._helpers import _assistant_calendar_text, _journal_text


def s19_appeal_deadlines(env) -> bool:
    text = _assistant_calendar_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_second = any(key in text for key in ("二审", "被上诉", "上诉"))
    has_response = any(key in text for key in ("答辩", "应诉", "举证"))
    has_deadline = any(key in text for key in ("期限", "截止", "15日", "十五日", "2026-07"))
    return has_second and has_response and has_deadline


def s19_appeal_vs_trial(env) -> bool:
    text = _journal_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_role = "被上诉人" in text
    has_scope = any(key in text for key in ("围绕上诉请求", "上诉请求范围", "二审审理范围"))
    has_evidence = any(key in text for key in ("证据目录", "一审证据", "补充证据", "举证期限"))
    has_cost = any(key in text for key in ("诉讼费", "费用", "预交"))
    return has_role and has_scope and has_evidence and has_cost


CHECKS = [
    ("s19_assistant_appeal_deadlines", s19_appeal_deadlines, 0.5),
    ("s19_persisted_second_instance_plan", s19_appeal_vs_trial, 0.5),
]
