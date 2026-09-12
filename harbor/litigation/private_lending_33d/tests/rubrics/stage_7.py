"""Stage 7: CJK_7BA1_CJK_8F96_CJK_6743_CJK_5F02_CJK_8BAE_ — CJK_65B0_CJK_9001_CJK_8FBE_CJK_5FC5_CJK_987B_CJK_89E6_CJK_53D1_CJK_6301_CJK_4E45_CJK_5316_CJK_56DE_CJK_5E94_。"""
from __future__ import annotations

from ._helpers import _journal_text, _notifications


def s7_detects_objection(env) -> bool:
    notifications = _notifications(env)
    if notifications is None:
        return False  # required evidence unavailable -> fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_lending_s7_jurisdiction"
        or (
            "CJK_7BA1_CJK_8F96_" in str(item.get("title") or "")
            and "CJK_5B81_CJK_6CE2_" in str(item.get("body") or "")
        )
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_followup = (
        any(key in journal for key in ("CJK_7BA1_CJK_8F96_CJK_6743_CJK_5F02_CJK_8BAE_", "CJK_7BA1_CJK_8F96_CJK_5F02_CJK_8BAE_"))
        and any(key in journal for key in ("CJK_4E66_CJK_9762_CJK_56DE_CJK_5E94_", "CJK_63D0_CJK_4EA4_CJK_610F_CJK_89C1_", "CJK_56DE_CJK_5E94_CJK_65B9_CJK_6848_", "CJK_53CD_CJK_9A73_"))
        and any(key in journal for key in ("CJK_63A5_CJK_6536_CJK_8D27_CJK_5E01_CJK_4E00_CJK_65B9_", "CJK_897F_CJK_6E56_CJK_533A_CJK_6CD5_CJK_9662_", "CJK_676D_CJK_5DDE_CJK_7BA1_CJK_8F96_"))
    )
    return has_notice and has_followup


CHECKS = [
    ("s7_objection_notice_and_followup", s7_detects_objection, 0.5),
]
