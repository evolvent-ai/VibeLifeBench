"""Stage 8: CJK_6848_CJK_4EF6_CJK_53D7_CJK_7406_ — CJK_53D7_CJK_7406_CJK_9001_CJK_8FBE_CJK_540E_CJK_9700_CJK_7559_CJK_5B58_CJK_6848_CJK_53F7_CJK_548C_CJK_4E0B_CJK_4E00_CJK_6B65_CJK_5B89_CJK_6392_。"""
from __future__ import annotations

from ._helpers import _assistant_calendar_text, _journal_text, _notifications


def s8_acceptance_followup(env) -> bool:
    notifications = _notifications(env)
    if notifications is None:
        return False  # required evidence unavailable -> fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_lending_s8_accepted"
        or "CJK_5DF2_CJK_53D7_CJK_7406_" in str(item.get("title") or "")
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _journal_text(env)
    calendar = _assistant_calendar_text(env)
    if journal is None or calendar is None:
        return False  # required evidence unavailable -> fail closed
    has_docket = "（2026）CJK_6D59_0106CJK_6C11_CJK_521D_08812CJK_53F7_" in journal or "CJK_6D59_0106CJK_6C11_CJK_521D_08812" in journal
    has_next = any(key in f"{journal} {calendar}" for key in ("CJK_4E3E_CJK_8BC1_", "CJK_7A0B_CJK_5E8F_CJK_610F_CJK_89C1_", "CJK_5F00_CJK_5EAD_", "CJK_9001_CJK_8FBE_CJK_6838_CJK_5BF9_"))
    return has_notice and has_docket and has_next


CHECKS = [
    ("s8_acceptance_and_persisted_followup", s8_acceptance_followup, 0.5),
]
