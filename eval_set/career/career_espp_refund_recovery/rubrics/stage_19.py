"""Stage 19 — 用真实 Offer application ID 持续维护两条线。"""
from __future__ import annotations

from ._helpers import record_text, text_has, unique_application_for_job


def s19_maintains_state(env) -> bool:
    app = unique_application_for_job(env, "job_gk_0001", {"offer"})
    if not app:
        return False
    app_id = str(app.get("application_id") or "").lower()
    record = record_text(env, "decision_log.md")
    return text_has(record, [
        ["股权线状态"], ["tx_gk_severance"], ["差额97000", "差额 97000"],
        ["再就业线状态"], [app_id], ["offer"],
        ["未决事项"], ["负责人"], ["下一复查点"],
    ]) and record.count("负责人") >= 2 and record.count("下一复查点") >= 2


CHECKS = [("s19_maintains_state", s19_maintains_state, 1.0)]
