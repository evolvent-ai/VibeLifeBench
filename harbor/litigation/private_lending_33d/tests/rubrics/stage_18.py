"""Stage 18: CJK_88AB_CJK_544A_CJK_4E0A_CJK_8BC9_ — CJK_4E8C_CJK_5BA1_CJK_9001_CJK_8FBE_CJK_987B_CJK_89E6_CJK_53D1_CJK_88AB_CJK_4E0A_CJK_8BC9_CJK_4EBA_CJK_51C6_CJK_5907_。"""
from __future__ import annotations

from ._helpers import _journal_text, _notifications


def s18_appeal_response_prepared(env) -> bool:
    notifications = _notifications(env)
    if notifications is None:
        return False  # required evidence unavailable -> fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_lending_s18_appeal"
        or "CJK_4E0A_CJK_8BC9_" in str(item.get("title") or "")
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_role = "CJK_88AB_CJK_4E0A_CJK_8BC9_CJK_4EBA_" in journal and any(key in journal for key in ("CJK_9648_CJK_5F3A_CJK_4E0A_CJK_8BC9_", "CJK_4E8C_CJK_5BA1_", "CJK_4E0A_CJK_8BC9_CJK_72B6_"))
    has_action = any(key in journal for key in ("CJK_7B54_CJK_8FA9_", "CJK_8BC1_CJK_636E_CJK_76EE_CJK_5F55_", "CJK_4E8C_CJK_5BA1_CJK_51C6_CJK_5907_", "CJK_5E94_CJK_8BC9_"))
    return has_notice and has_role and has_action


CHECKS = [
    ("s18_appeal_notice_and_persisted_response", s18_appeal_response_prepared, 0.5),
]
