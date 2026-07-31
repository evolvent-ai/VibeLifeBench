"""Stage 10: 被告答辩静默送达 — 新通知必须触发持久化质证准备。"""
from __future__ import annotations

from ._helpers import _food_journal_text, _notifications


def s10_detects_defense(env) -> bool:
    """答辩通知存在，且协作者在 Notion 留下逐项核对/质证行动。"""
    notifications = _notifications(env)
    if notifications is None:
        return False  # required evidence unavailable -> fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_food_s10_defense"
        or (
            "答辩" in str(item.get("title") or "")
            and any(key in str(item.get("body") or "") for key in ("知假买假", "标签瑕疵", "退一赔三"))
        )
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _food_journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_followup = (
        any(key in journal for key in ("答辩", "抗辩"))
        and any(key in journal for key in ("质证", "逐项核对", "反驳", "补强证据"))
        and sum(key in journal for key in ("退一赔三", "知假买假", "标签瑕疵")) >= 2
    )
    return has_notice and has_followup


CHECKS = [
    ("s10_defense_notice_and_followup", s10_detects_defense, 0.75),
]
