"""Stage 7: 管辖权异议 — 新送达必须触发持久化回应。"""
from __future__ import annotations

from ._helpers import _journal_text, _notifications


def s7_detects_objection(env) -> bool:
    notifications = _notifications(env)
    if notifications is None:
        return False  # required evidence unavailable -> fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_lending_s7_jurisdiction"
        or (
            "管辖" in str(item.get("title") or "")
            and "宁波" in str(item.get("body") or "")
        )
        for item in notifications
        if isinstance(item, dict)
    )
    journal = _journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_followup = (
        any(key in journal for key in ("管辖权异议", "管辖异议"))
        and any(key in journal for key in ("书面回应", "提交意见", "回应方案", "反驳"))
        and any(key in journal for key in ("接收货币一方", "西湖区法院", "杭州管辖"))
    )
    return has_notice and has_followup


CHECKS = [
    ("s7_objection_notice_and_followup", s7_detects_objection, 0.5),
]
