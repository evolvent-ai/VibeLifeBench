"""Stage 7 — 在安静期维护明确的监控对象和复查点。"""
from __future__ import annotations

from ._helpers import record_text, text_has


def s7_quiet_monitor(env) -> bool:
    record = record_text(env, "decision_log.md")
    return text_has(record, [
        ["监控对象"], ["hr", "公司"], ["暂无新增", "无新增", "未有新增"],
        ["下一复查点", "下次复查"], ["收件箱", "邮件"],
    ])


CHECKS = [("s7_quiet_monitor", s7_quiet_monitor, 1.0)]
