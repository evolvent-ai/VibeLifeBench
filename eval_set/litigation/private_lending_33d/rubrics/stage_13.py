"""Stage 13: 律师利益冲突退出 — 通知与代理交接行动必须同时存在。"""
from __future__ import annotations

from ._helpers import _assistant_calendar_text, _journal_text, _notifications
from .cross_stage import d_lawyer_reselect


def s13_detects_withdrawal(env) -> bool:
    notifications = _notifications(env)
    if notifications is None:
        return False  # required evidence unavailable -> fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_lending_s13_lawyer"
        or (
            "利益冲突" in f"{item.get('title', '')} {item.get('body', '')}"
            and "退出" in f"{item.get('title', '')} {item.get('body', '')}"
        )
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_followup = (
        any(key in journal for key in ("周敏", "LD-006", "利益冲突"))
        and any(key in journal for key in ("LD-008", "钱蕾"))
        and any(key in journal for key in ("改选", "另行委托", "交接"))
    )
    return has_notice and has_followup


def s13_hearing_not_delayed(env) -> bool:
    journal = _journal_text(env)
    calendar = _assistant_calendar_text(env)
    if journal is None or calendar is None:
        return False  # required evidence unavailable -> fail closed
    has_change = any(key in journal for key in ("LD-008", "钱蕾", "新律师", "材料交接"))
    has_continuity = any(key in journal for key in ("不耽误", "如期", "按时", "交接", "证据原件"))
    has_hearing = (
        any(key in calendar for key in ("开庭", "庭审", "庭前"))
        and any(key in calendar for key in ("6月12", "2026-06-12", "06-12"))
    )
    return has_change and has_hearing and has_continuity


CHECKS = [
    ("s13_withdrawal_notice_and_followup", s13_detects_withdrawal, 0.5),
    ("s13_hearing_continuity_persisted", s13_hearing_not_delayed, 0.5),
    ("d_lawyer_reselect", d_lawyer_reselect, 3.667),
]
