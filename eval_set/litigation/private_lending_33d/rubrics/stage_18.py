"""Stage 18: 被告上诉 — 二审送达须触发被上诉人准备。"""
from __future__ import annotations

from ._helpers import _journal_text, _notifications


def s18_appeal_response_prepared(env) -> bool:
    notifications = _notifications(env)
    if notifications is None:
        return False  # required evidence unavailable -> fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_lending_s18_appeal"
        or "上诉" in str(item.get("title") or "")
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_role = "被上诉人" in journal and any(key in journal for key in ("陈强上诉", "二审", "上诉状"))
    has_action = any(key in journal for key in ("答辩", "证据目录", "二审准备", "应诉"))
    return has_notice and has_role and has_action


CHECKS = [
    ("s18_appeal_notice_and_persisted_response", s18_appeal_response_prepared, 0.5),
]
