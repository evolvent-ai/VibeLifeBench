"""Stage 13: CJK_5F8B_CJK_5E08_CJK_5229_CJK_76CA_CJK_51B2_CJK_7A81_CJK_9000_CJK_51FA_ — CJK_901A_CJK_77E5_CJK_4E0E_CJK_4EE3_CJK_7406_CJK_4EA4_CJK_63A5_CJK_884C_CJK_52A8_CJK_5FC5_CJK_987B_CJK_540C_CJK_65F6_CJK_5B58_CJK_5728_。"""
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
            "CJK_5229_CJK_76CA_CJK_51B2_CJK_7A81_" in f"{item.get('title', '')} {item.get('body', '')}"
            and "CJK_9000_CJK_51FA_" in f"{item.get('title', '')} {item.get('body', '')}"
        )
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_followup = (
        any(key in journal for key in ("CJK_5468_CJK_654F_", "LD-006", "CJK_5229_CJK_76CA_CJK_51B2_CJK_7A81_"))
        and any(key in journal for key in ("LD-008", "CJK_94B1_CJK_857E_"))
        and any(key in journal for key in ("CJK_6539_CJK_9009_", "CJK_53E6_CJK_884C_CJK_59D4_CJK_6258_", "CJK_4EA4_CJK_63A5_"))
    )
    return has_notice and has_followup


def s13_hearing_not_delayed(env) -> bool:
    journal = _journal_text(env)
    calendar = _assistant_calendar_text(env)
    if journal is None or calendar is None:
        return False  # required evidence unavailable -> fail closed
    has_change = any(key in journal for key in ("LD-008", "CJK_94B1_CJK_857E_", "CJK_65B0_CJK_5F8B_CJK_5E08_", "CJK_6750_CJK_6599_CJK_4EA4_CJK_63A5_"))
    has_continuity = any(key in journal for key in ("CJK_4E0D_CJK_803D_CJK_8BEF_", "CJK_5982_CJK_671F_", "CJK_6309_CJK_65F6_", "CJK_4EA4_CJK_63A5_", "CJK_8BC1_CJK_636E_CJK_539F_CJK_4EF6_"))
    has_hearing = (
        any(key in calendar for key in ("CJK_5F00_CJK_5EAD_", "CJK_5EAD_CJK_5BA1_", "CJK_5EAD_CJK_524D_"))
        and any(key in calendar for key in ("6CJK_6708_12", "2026-06-12", "06-12"))
    )
    return has_change and has_hearing and has_continuity


CHECKS = [
    ("s13_withdrawal_notice_and_followup", s13_detects_withdrawal, 0.5),
    ("s13_hearing_continuity_persisted", s13_hearing_not_delayed, 0.5),
    ("d_lawyer_reselect", d_lawyer_reselect, 3.667),
]
