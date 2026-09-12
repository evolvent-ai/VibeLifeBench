"""Stage 10: CJK_88AB_CJK_544A_CJK_7B54_CJK_8FA9_ — CJK_65B0_CJK_9001_CJK_8FBE_CJK_5FC5_CJK_987B_CJK_89E6_CJK_53D1_CJK_6301_CJK_4E45_CJK_5316_CJK_8D28_CJK_8BC1_CJK_51C6_CJK_5907_。"""
from __future__ import annotations

from ._helpers import _journal_text, _notifications


def s10_detects_defense(env) -> bool:
    notifications = _notifications(env)
    if notifications is None:
        return False  # required evidence unavailable -> fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_lending_s10_defense"
        or (
            "CJK_7B54_CJK_8FA9_" in str(item.get("title") or "")
            and any(key in str(item.get("body") or "") for key in ("36CJK_4E07_CJK_5143_", "CJK_73B0_CJK_91D1_", "CJK_5B9E_CJK_9645_CJK_5230_CJK_8D26_"))
        )
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_followup = (
        any(key in journal for key in ("CJK_7B54_CJK_8FA9_", "CJK_8D28_CJK_8BC1_"))
        and any(key in journal for key in ("36CJK_4E07_", "360000", "CJK_5B9E_CJK_9645_CJK_5230_CJK_8D26_"))
        and any(key in journal for key in ("20CJK_4E07_CJK_73B0_CJK_91D1_", "CJK_73B0_CJK_91D1_CJK_4EA4_CJK_4ED8_", "CJK_53D6_CJK_73B0_CJK_51ED_CJK_8BC1_"))
        and any(key in journal for key in ("CJK_63A5_CJK_53D7_", "CJK_53CD_CJK_9A73_", "CJK_8865_CJK_5F3A_", "CJK_4E3E_CJK_8BC1_CJK_98CE_CJK_9669_"))
    )
    return has_notice and has_followup


CHECKS = [
    ("s10_defense_notice_and_followup", s10_detects_defense, 0.5),
]
