"""Stage 12: 开庭通知 — 检查协作者自行持久化的庭前安排。"""
from __future__ import annotations

from ._helpers import _assistant_calendar_text, _journal_text


def s12_hearing_on_calendar(env) -> bool:
    text = _assistant_calendar_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_hearing = any(key in text for key in ("开庭", "庭审", "庭前"))
    has_date = any(key in text for key in ("2026-06-12", "06-12", "6月12"))
    return has_hearing and has_date


def s12_brings_originals(env) -> bool:
    journal = _journal_text(env)
    calendar = _assistant_calendar_text(env)
    if journal is None or calendar is None:
        return False  # required evidence unavailable -> fail closed
    has_id = any(key in journal for key in ("身份证", "证件"))
    has_note = any(key in journal for key in ("借条原件", "借条", "证据原件"))
    has_bank = any(key in journal for key in ("转账回单", "银行流水", "电子回单"))
    has_chat = any(key in journal for key in ("微信记录", "催收记录", "还款记录"))
    has_hearing_calendar = (
        any(key in calendar for key in ("开庭", "庭审", "庭前"))
        and any(key in calendar for key in ("2026-06-12", "06-12", "6月12"))
    )
    return has_id and has_note and has_bank and has_chat and has_hearing_calendar


CHECKS = [
    ("s12_assistant_hearing_calendar", s12_hearing_on_calendar, 0.5),
    ("s12_persisted_originals_checklist", s12_brings_originals, 0.5),
]
