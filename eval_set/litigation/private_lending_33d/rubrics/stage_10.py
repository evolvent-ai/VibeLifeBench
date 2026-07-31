"""Stage 10: 被告答辩 — 新送达必须触发持久化质证准备。"""
from __future__ import annotations

from ._helpers import _journal_text, _notifications


def s10_detects_defense(env) -> bool:
    notifications = _notifications(env)
    if notifications is None:
        return False  # required evidence unavailable -> fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_lending_s10_defense"
        or (
            "答辩" in str(item.get("title") or "")
            and any(key in str(item.get("body") or "") for key in ("36万元", "现金", "实际到账"))
        )
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_followup = (
        any(key in journal for key in ("答辩", "质证"))
        and any(key in journal for key in ("36万", "360000", "实际到账"))
        and any(key in journal for key in ("20万现金", "现金交付", "取现凭证"))
        and any(key in journal for key in ("接受", "反驳", "补强", "举证风险"))
    )
    return has_notice and has_followup


CHECKS = [
    ("s10_defense_notice_and_followup", s10_detects_defense, 0.5),
]
