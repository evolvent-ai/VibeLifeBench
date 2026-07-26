"""Stage 12: 开庭送达 — 检查协作者自行持久化的庭前安排。"""
from __future__ import annotations

from ._helpers import _assistant_calendar_text, _food_journal_text


def s12_hearing_in_calendar(env) -> bool:
    """协作者创建的日历事项包含 2026-06-12 开庭或庭前准备。"""
    text = _assistant_calendar_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_hearing = any(key in text for key in ("开庭", "庭审", "庭前"))
    has_date = any(key in text for key in ("2026-06-12", "06-12", "6月12"))
    return has_hearing and has_date


def s12_bring_originals(env) -> bool:
    """庭前清单已持久化，覆盖原件、食品实物和检验材料。"""
    journal = _food_journal_text(env)
    calendar = _assistant_calendar_text(env)
    if journal is None or calendar is None:
        return False  # required evidence unavailable -> fail closed
    has_originals = any(key in journal for key in ("证据原件", "原件", "身份证"))
    has_food = any(key in journal for key in ("食品实物", "涉案食品", "奶粉", "代用茶"))
    has_inspection = any(key in journal for key in ("检验材料", "检验报告", "送检"))
    has_hearing_calendar = (
        any(key in calendar for key in ("开庭", "庭审", "庭前"))
        and any(key in calendar for key in ("2026-06-12", "06-12", "6月12"))
    )
    return has_originals and has_food and has_inspection and has_hearing_calendar


CHECKS = [
    ("s12_assistant_hearing_calendar", s12_hearing_in_calendar, 0.5),
    ("s12_persisted_originals_checklist", s12_bring_originals, 0.5),
]
