"""Stage 8: 案件受理 — 受理送达后需留存案号和下一步安排。"""
from __future__ import annotations

from ._helpers import _assistant_calendar_text, _journal_text, _notifications


def s8_acceptance_followup(env) -> bool:
    notifications = _notifications(env)
    if notifications is None:
        return False  # required evidence unavailable -> fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_lending_s8_accepted"
        or "已受理" in str(item.get("title") or "")
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _journal_text(env)
    calendar = _assistant_calendar_text(env)
    if journal is None or calendar is None:
        return False  # required evidence unavailable -> fail closed
    has_docket = "（2026）浙0106民初08812号" in journal or "浙0106民初08812" in journal
    has_next = any(key in f"{journal} {calendar}" for key in ("举证", "程序意见", "开庭", "送达核对"))
    return has_notice and has_docket and has_next


CHECKS = [
    ("s8_acceptance_and_persisted_followup", s8_acceptance_followup, 0.5),
]
